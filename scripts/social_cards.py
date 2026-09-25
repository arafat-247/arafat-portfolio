"""Create deterministic article-specific Open Graph cards during the site build."""
from hashlib import sha256
from html.parser import HTMLParser
from io import BytesIO
from pathlib import Path, PurePosixPath
from urllib.parse import urljoin

from PIL import Image, ImageDraw, ImageFont, ImageOps

from core import fetch

WIDTH, HEIGHT = 1200, 630
INK = (248, 246, 239)
MUTED = (199, 214, 208)
ACCENT = (238, 101, 75)
GREEN = (2, 71, 53)

SERIF_FONTS = (
    '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',
    '/usr/share/fonts/opentype/urw-base35/NimbusRoman-Bold.otf',
)
SANS_FONTS = (
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/opentype/urw-base35/NimbusSans-Regular.otf',
)
SANS_BOLD_FONTS = (
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/opentype/urw-base35/NimbusSans-Bold.otf',
)


class OgImageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.image=''

    def handle_starttag(self,tag,attrs):
        if tag.lower()!='meta' or self.image:return
        attrs=dict(attrs)
        key=(attrs.get('property') or attrs.get('name') or '').lower()
        if key in ('og:image','og:image:url','twitter:image','twitter:image:src'):
            self.image=(attrs.get('content') or '').strip()


def load_font(candidates, size):
    for candidate in candidates:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default(size=size)


def wrap(draw, text, font, width):
    lines=[]
    for word in str(text or '').split():
        trial=' '.join((lines[-1],word)).strip() if lines else word
        if lines and draw.textlength(trial,font=font)>width:
            lines.append(word)
        elif lines:
            lines[-1]=trial
        else:
            lines=[word]
    return lines or ['Untitled']


def fit_headline(draw, text, width, height):
    for size in range(66,27,-2):
        font=load_font(SERIF_FONTS,size)
        lines=wrap(draw,text,font,width)
        spacing=max(5,size//8)
        line_height=draw.textbbox((0,0),'Ag',font=font)[3]
        if len(lines)<=6 and len(lines)*line_height+(len(lines)-1)*spacing<=height:
            return font,lines,spacing
    font=load_font(SERIF_FONTS,28);lines=wrap(draw,text,font,width)[:6]
    if len(wrap(draw,text,font,width))>6:
        while draw.textlength(lines[-1]+'…',font=font)>width and lines[-1]:
            lines[-1]=lines[-1][:-1].rstrip()
        lines[-1]+='…'
    return font,lines,5


def clean_label(value,limit):
    value=' '.join(str(value or '').split())
    return value if len(value)<=limit else value[:limit-1].rstrip()+'…'


def filename_for(article):
    slug=PurePosixPath(str(article.get('local_url','')).rstrip('/')).name or 'article'
    signature='|'.join(str(article.get(key,'')) for key in ('title','category','stream','date_published','source_name','source_url','source_image','cover_image'))
    digest=sha256(signature.encode('utf-8')).hexdigest()[:8]
    return f'{slug}-{digest}.jpg'


def looks_generic(url):
    value=str(url or '').lower()
    return any(token in value for token in ('logo','favicon','placeholder','default-image','default_image','social-share','social_share','share-default','share_default'))


class SocialCardRenderer:
    def __init__(self,template,output):
        self.template=Path(template);self.output=Path(output);self._base=None
        self.site_root=self.template.parent.parent

    def base(self):
        if self._base is None:
            image=Image.open(self.template).convert('RGB').resize((WIDTH,HEIGHT),Image.Resampling.LANCZOS)
            # The portrait remains untouched. A soft green veil clears the
            # former generic copy and creates a legible field in the gaze line.
            veil=Image.new('RGB',(WIDTH,HEIGHT),GREEN);mask=Image.new('L',(WIDTH,HEIGHT),0)
            pixels=mask.load()
            for x in range(500,WIDTH):
                alpha=min(255,max(0,round((x-500)/90*255)))
                for y in range(HEIGHT):pixels[x,y]=alpha
            self._base=Image.composite(veil,image,mask)
        return self._base.copy()

    def local_story_image(self,article):
        cover=str(article.get('cover_image') or '').strip().lstrip('/')
        if not cover:return None
        path=(self.site_root/cover).resolve()
        try:path.relative_to(self.site_root.resolve())
        except ValueError:return None
        if not path.is_file():return None
        try:return Image.open(path).convert('RGB')
        except OSError:return None

    def remote_story_image(self,article):
        candidates=[]
        source_image=str(article.get('source_image') or '').strip()
        if source_image:candidates.append(source_image)
        source_url=str(article.get('source_url') or '').strip()
        if source_url and not candidates:
            try:
                data,typ,final=fetch(source_url,2_000_000)
                if typ in ('text/html','application/xhtml+xml'):
                    parser=OgImageParser();parser.feed(data.decode('utf-8',errors='replace'))
                    if parser.image:candidates.append(urljoin(final,parser.image))
            except (OSError,ValueError):
                pass
        for candidate in candidates:
            if not candidate or looks_generic(candidate):continue
            try:
                data,typ,_=fetch(candidate,8_000_000)
                if not typ.startswith('image/'):continue
                image=Image.open(BytesIO(data)).convert('RGB')
                if image.width<480 or image.height<270 or image.width*image.height<250000:continue
                return image
            except (OSError,ValueError):
                continue
        return None

    def story_image(self,article):
        return self.local_story_image(article) or self.remote_story_image(article)

    def story_base(self,story):
        image=Image.new('RGB',(WIDTH,HEIGHT),GREEN)
        photo=ImageOps.fit(story,(620,HEIGHT),method=Image.Resampling.LANCZOS,centering=(0.5,0.5))
        image.paste(photo,(0,0))
        veil=Image.new('RGB',(WIDTH,HEIGHT),GREEN);mask=Image.new('L',(WIDTH,HEIGHT),0)
        pixels=mask.load()
        for x in range(540,681):
            alpha=min(255,max(0,round((x-540)/140*255)))
            for y in range(HEIGHT):pixels[x,y]=alpha
        return Image.composite(veil,image,mask)

    def render(self,article):
        self.output.mkdir(parents=True,exist_ok=True)
        filename=filename_for(article);target=self.output/filename
        if target.is_file():return 'assets/social/'+filename

        story=self.story_image(article)
        image=self.story_base(story) if story else self.base()
        draw=ImageDraw.Draw(image)

        stream={'reporting':'REPORTING','opinion':'OPINION & ANALYSIS','thoughts':'THOUGHTS'}.get(article.get('stream'),'PORTFOLIO')
        category=clean_label(article.get('category'),28).upper()
        eyebrow=stream+(f'  •  {category}' if category and category!=stream else '')
        draw.text((680,70),eyebrow,font=load_font(SANS_BOLD_FONTS,18),fill=ACCENT)
        draw.rounded_rectangle((680,108,774,114),radius=3,fill=ACCENT)

        font,lines,spacing=fit_headline(draw,article.get('title'),470,350)
        y=139
        for line in lines:
            draw.text((680,y),line,font=font,fill=INK,stroke_width=1,stroke_fill=(8,61,48))
            y+=draw.textbbox((0,0),'Ag',font=font)[3]+spacing

        draw.line((680,522,1140,522),fill=(91,139,124),width=1)
        draw.text((680,542),'ARAFAT RAHAMAN',font=load_font(SANS_BOLD_FONTS,20),fill=INK)
        source=clean_label(article.get('source_name') or ('Personal essay' if article.get('stream')=='thoughts' else 'The Daily Star'),30)
        draw.text((680,573),source,font=load_font(SANS_FONTS,16),fill=MUTED)
        date=str(article.get('date_published',''))[:10]
        if date:
            try:
                year,month,day=date.split('-');date=f'{int(day)}.{int(month)}.{year}'
            except ValueError:pass
        date_font=load_font(SANS_FONTS,16)
        draw.text((1140-draw.textlength(date,font=date_font),573),date,font=date_font,fill=MUTED)

        image.save(target,'JPEG',quality=84,optimize=True,progressive=True,subsampling=2)
        return 'assets/social/'+filename
