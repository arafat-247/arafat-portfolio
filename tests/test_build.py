import contextlib, io, json, re, shutil, sys, tempfile, unittest
from pathlib import Path
from PIL import Image
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build, core, sync
from types import SimpleNamespace
from urllib.error import HTTPError

class BuildTests(unittest.TestCase):
    def test_credit_classification_respects_editorial_override(self):
        manual={'manual_import':True,'verified_author':False}
        self.assertEqual(build.credit_type(manual),'contribution')
        self.assertEqual(build.credit_type({**manual,'credit_type_override':'author-page'}),'byline')
        self.assertEqual(build.credit_type({'verified_author':True}),'byline')

    def test_discovery_reads_every_author_card(self):
        source=b'''<article class="article-author"><a href="/news/first-12345">One</a></article>
        <article class="article-author featured"><a href="https://www.thedailystar.net/news/second-67890">Two</a></article>'''
        with patch('sync.fetch',return_value=(source,'text/html','https://www.thedailystar.net/author/arafat-rahaman')):
            self.assertEqual(sync.discover('https://www.thedailystar.net/author/arafat-rahaman'),[
                'https://www.thedailystar.net/news/first-12345',
                'https://www.thedailystar.net/news/second-67890'])

    def test_drafts_and_attribution(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp); content=base/'content'; site=base/'site'; out=base/'dist'
            site.mkdir();content.mkdir();shutil.copytree(core.SITE/'assets',site/'assets');shutil.copytree(core.SITE/'admin',site/'admin')
            for n in ('portfolio.js','portfolio.css'):shutil.copy2(core.SITE/n,site/n)
            core.write(content/'settings.json',core.read(core.CONTENT/'settings.json'))
            cover=site/'assets/uploads/draft-only.webp';cover.parent.mkdir(exist_ok=True);shutil.copy2(site/'assets/identity/asset0.webp',cover)
            core.write(content/'photos.json',{'photos':[{
                'id':'photo','src':'assets/identity/asset0.webp','caption':'Dhaka after rain',
                'alt':'A street in Dhaka after rain','location':'Dhaka','status':'published'}]})
            common={'stream':'thoughts','category':'Essays','date_published':'2026-09-05T10:00:00+06:00','body':'A complete personal essay.'}
            draft={**common,'id':'draft','title':'PRIVATE-DRAFT-CANARY','status':'draft','cover_image':'assets/uploads/draft-only.webp'}
            published={**common,'id':'essay','title':'Published essay','status':'published','format':'html','body':'<p>Public text.</p><script>ATTACK_CANARY()</script>'}
            core.write(content/'posts.json',{'posts':[draft,published]})
            imported={'id':'abc123','title':'A shared report','status':'published','stream':'reporting','category':'News','date_published':'2026-09-04T10:00:00+06:00','body_html':'<p>Authorised archived report.</p>','source_url':'https://example.com/a','source_name':'Example publication','original_authors':['Staff Correspondent'],'manual_import':True,'verified_author':False,'contribution':'Co-reporting','local_url':'stories/abc123-report/'}
            core.write(content/'articles/abc123.json',imported)
            with patch.multiple(build,CONTENT=content,SITE=site,OUT=out),contextlib.redirect_stdout(io.StringIO()):build.build()
            visible=''.join(p.read_text() for p in out.rglob('*.html'))+(out/'data/index.json').read_text()
            self.assertNotIn('PRIVATE-DRAFT-CANARY',visible);self.assertNotIn('ATTACK_CANARY',visible)
            self.assertFalse((out/'assets/uploads/draft-only.webp').exists())
            self.assertFalse((out/'content').exists())
            story=(out/'stories/a-shared-report/index.html').read_text()
            self.assertIn('Staff Correspondent',story);self.assertIn('Non-byline contribution by Arafat Rahaman',story)
            self.assertNotIn('"name": "Arafat Rahaman"',story)
            self.assertIn('<meta property="og:type" content="article">',story)
            self.assertIn('twitter:card" content="summary_large_image"',story)
            social_match=re.search(r'https://arafatrahaman\.com/(assets/social/a-shared-report-[0-9a-f]{8}\.jpg)',story)
            self.assertIsNotNone(social_match)
            social_card=out/social_match.group(1)
            self.assertTrue(social_card.is_file())
            with Image.open(social_card) as card:self.assertEqual(card.size,(1200,630))
            self.assertIn('id="share-dialog"',story)
            self.assertIn('data-share-service="facebook"',story)
            self.assertIn('data-copy-share',story)
            self.assertNotIn('/about/#person',story)
            self.assertIn('https://arafatrahaman.com/stories/a-shared-report/',story)
            authored=(out/'thoughts/published-essay/index.html').read_text()
            self.assertIn('https://arafatrahaman.com/about/#person',authored)
            about=(out/'about/index.html').read_text()
            self.assertEqual(about.count('googletagmanager.com/gtag/js?id=G-MHCDNYZYP9'),1)
            self.assertEqual(about.count("gtag('config','G-MHCDNYZYP9')"),1)
            self.assertIn('"@type": "ProfilePage"',about)
            self.assertIn('"mainEntity": {"@type": "Person"',about)
            self.assertIn('"image": "https://arafatrahaman.com/assets/identity/asset0.webp"',about)
            self.assertIn('"knowsAbout": ["Education"',about)
            redirect=(out/'stories/abc123-report/index.html').read_text()
            self.assertIn('noindex,follow',redirect);self.assertIn('/stories/a-shared-report/',redirect)
            self.assertEqual((out/'CNAME').read_text(),'arafatrahaman.com\n')
            sitemap=(out/'sitemap.xml').read_text()
            self.assertIn('https://arafatrahaman.com/stories/a-shared-report/</loc>',sitemap)
            self.assertNotIn('/index.html</loc>',sitemap)
            home=(out/'index.html').read_text()
            self.assertIn('Selected paths through my work',home)
            self.assertIn('<h1>Portfolio</h1>',home)
            self.assertIn("location.pathname.endsWith('/index.html')",home)
            self.assertIn('News reports, interviews and reported features',home)
            self.assertNotIn('class="recentwork"',home)
            self.assertNotIn('Latest journalism',home)
            self.assertEqual(home.count('class="tile-art"'),3)
            self.assertRegex(home,r'class="tile tile-photos"[^>]*><img ')
            self.assertIn('class="themetoggle"',home)
            self.assertIn('class="menutoggle"',home)
            client_css=(out/'portfolio.css').read_text()
            self.assertIn('.home .menutoggle,.inner .themetoggle{display:none}',client_css)
            self.assertIn('.home .mobilemenu,.home .menubackdrop{display:none!important}',client_css)
            self.assertNotIn('src=""',home)
            client=(out/'portfolio.js').read_text()
            self.assertIn('if(!menu)return;',client)
            reporting=(out/'reporting/index.html').read_text()
            self.assertIn('<h1>Reports & Features</h1>',reporting)
            self.assertIn('data-total="byline">0',reporting)
            self.assertIn('data-total="contribution">1',reporting)
            self.assertIn('name="credit"',reporting)
            self.assertIn('Non-byline contribution',reporting)
            self.assertIn('class="menutoggle"',reporting)
            self.assertIn('class="themetoggle"',reporting)
            self.assertIn('id="mobile-menu"',reporting)
            photography=(out/'photography/index.html').read_text()
            self.assertIn('class="photodialog"',photography)
            self.assertIn('data-prev-photo',photography)
            self.assertIn('data-next-photo',photography)
            self.assertIn('data-dialog-caption',photography)
            self.assertIn('data-photo-view="mosaic"',photography)
            self.assertIn('data-photo-view="grid"',photography)
            self.assertIn('loading="eager"',photography)
            self.assertIn('../assets/identity/asset0.webp',photography)
            self.assertIn('https://arafatrahaman.com/photography/',photography)
            self.assertTrue((out/'reporting.html').is_file())
            self.assertIn('https://arafatrahaman.com/reporting/',(out/'reporting.html').read_text())
    def test_source_failure_preserves_article(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);u='https://www.thedailystar.net/news/example-12345';key=core.identity(u)
            old={'id':key,'title':'Saved report','body_html':'<p>Permanent body.</p>','word_count':200}
            core.write(root/'articles'/f'{key}.json',old)
            with patch('sync.CONTENT',root),patch('sync.discover',return_value=[u]),patch('sync.fetch',side_effect=HTTPError(u,404,'Gone',None,None)),contextlib.redirect_stdout(io.StringIO()):
                sync.run(SimpleNamespace(full=True,pages=1,limit=1,delay=0))
            self.assertEqual(core.read(root/'articles'/f'{key}.json'),old)
            self.assertEqual(core.read(root/'sync-state.json')['sources'][u]['status'],'failed')

if __name__=='__main__':unittest.main()
