"""Create deterministic article-specific Open Graph cards during the site build."""
from hashlib import sha256
from pathlib import Path, PurePosixPath

from PIL import Image, ImageDraw, ImageFont

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
    signature='|'.join(str(article.get(key,'')) for key in ('title','category','stream','date_published','source_name'))
    digest=sha256(signature.encode('utf-8')).hexdigest()[:8]
    return f'{slug}-{digest}.jpg'


class SocialCardRenderer:
    def __init__(self,template,output):
        self.template=Path(template);self.output=Path(output);self._base=None

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

    def render(self,article):
        self.output.mkdir(parents=True,exist_ok=True)
        filename=filename_for(article);target=self.output/filename
        if target.is_file():return 'assets/social/'+filename

        image=self.base()
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
