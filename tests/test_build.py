import contextlib, io, json, re, shutil, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build, core, sync
from types import SimpleNamespace
from urllib.error import HTTPError

class BuildTests(unittest.TestCase):
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
            core.write(content/'photos.json',{'photos':[]})
            common={'stream':'thoughts','category':'Essays','date_published':'2026-09-05T10:00:00+06:00','body':'A complete personal essay.'}
            draft={**common,'id':'draft','title':'PRIVATE-DRAFT-CANARY','status':'draft','cover_image':'assets/uploads/draft-only.webp'}
            published={**common,'id':'essay','title':'Published essay','status':'published','format':'html','body':'<p>Public text.</p><script>ATTACK_CANARY()</script>'}
            core.write(content/'posts.json',{'posts':[draft,published]})
            imported={'id':'abc123','title':'A shared report','status':'published','stream':'reporting','category':'News','date_published':'2026-09-04T10:00:00+06:00','body_html':'<p>Authorised archived report.</p>','source_url':'https://example.com/a','source_name':'Example publication','original_authors':['Staff Correspondent'],'manual_import':True,'verified_author':False,'author_listing_verified':False,'contribution':'Co-reporting','local_url':'stories/abc123-report/'}
            core.write(content/'articles/abc123.json',imported)
            with patch.multiple(build,CONTENT=content,SITE=site,OUT=out),contextlib.redirect_stdout(io.StringIO()):build.build()
            visible=''.join(p.read_text() for p in out.rglob('*.html'))+(out/'data/index.json').read_text()
            self.assertNotIn('PRIVATE-DRAFT-CANARY',visible);self.assertNotIn('ATTACK_CANARY',visible)
            self.assertFalse((out/'assets/uploads/draft-only.webp').exists())
            self.assertFalse((out/'content').exists())
            story=(out/'stories/a-shared-report/index.html').read_text()
            self.assertIn('Staff Correspondent',story);self.assertIn('Portfolio contribution: Arafat Rahaman',story)
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
            self.assertIn('https://arafatrahaman.com/stories/a-shared-report/',story)
            reporting=(out/'reporting/index.html').read_text()
            self.assertIn('<strong>0</strong><span>bylined stories</span>',reporting)
            self.assertIn('<strong>1</strong><span>non-byline contributions</span>',reporting)
            self.assertIn('name="credit"',reporting)
            self.assertIn('Non-byline contribution',reporting)
            index=core.read(out/'data/index.json')['articles']
            record=next(a for a in index if a['id']=='abc123')
            self.assertEqual(record['credit_type'],'contribution')
            self.assertEqual(record['contribution'],'Co-reporting')
            admin=(out/'admin/index.html').read_text()
            self.assertIn('id="import-stream"',admin)
            self.assertIn('id="import-credit"',admin)
            self.assertIn('Reports &amp; Features',admin)
            self.assertIn('id="import-category"',admin)
            self.assertIn('id="import-urls"',admin)
            self.assertIn('id="photo-batch"',admin)
            admin_js=(out/'admin/admin.js').read_text()
            self.assertIn('data-review-credit',admin_js)
            self.assertIn('credit_type_override',admin_js)
            self.assertIn('<option value="thoughts">Thoughts</option>',admin_js)
            self.assertIn('source=photo',admin_js)
            self.assertIn('save a fresh JPEG copy',admin_js)
            home=(out/'index.html').read_text()
            self.assertEqual(home.count('class="tile-art"'),3)
            self.assertRegex(home,r'class="tile tile-photos"[^>]*><img ')
            self.assertEqual(home.count('googletagmanager.com/gtag/js?id=G-MHCDNYZYP9'),1)
            self.assertIn("gtag('config','G-MHCDNYZYP9')",home)
            self.assertNotIn('googletagmanager.com',(out/'admin/index.html').read_text())
            self.assertIn('href="reporting/"',home)
            self.assertTrue((out/'about/index.html').is_file())
            self.assertTrue((out/'photography/index.html').is_file())
            self.assertIn('More photographs on Flickr', (out/'photography/index.html').read_text())
            self.assertIn('data-photo-next', (out/'photography/index.html').read_text())
            self.assertIn('/reporting/',(out/'reporting.html').read_text())
            redirect=(out/'stories/abc123-report/index.html').read_text()
            self.assertIn('noindex,follow',redirect);self.assertIn('/stories/a-shared-report/',redirect)
            self.assertEqual((out/'CNAME').read_text(),'arafatrahaman.com\n')
            sitemap=(out/'sitemap.xml').read_text()
            self.assertIn('https://arafatrahaman.com/stories/a-shared-report/</loc>',sitemap)
            self.assertNotIn('/index.html</loc>',sitemap)
    def test_source_failure_preserves_article(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);u='https://www.thedailystar.net/news/example-12345';key=core.identity(u)
            old={'id':key,'title':'Saved report','body_html':'<p>Permanent body.</p>','word_count':200}
            core.write(root/'articles'/f'{key}.json',old)
            with patch('sync.CONTENT',root),patch('sync.discover',return_value=[u]),patch('sync.fetch',side_effect=HTTPError(u,404,'Gone',None,None)),contextlib.redirect_stdout(io.StringIO()):
                sync.run(SimpleNamespace(full=True,pages=1,limit=1,delay=0))
            self.assertEqual(core.read(root/'articles'/f'{key}.json'),old)
            self.assertEqual(core.read(root/'sync-state.json')['sources'][u]['status'],'failed')

    def test_repeated_short_multimedia_extract_leaves_pending_queue(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);u='https://www.thedailystar.net/star-multimedia/news/example-12345'
            core.write(root/'sync-state.json',{'sources':{u:{'status':'failed','failures':3,'error':'Too little article text found; extraction rejected and logged.','last_checked':'2026-09-07T00:00:00+00:00'}},'listing_complete':True})
            with patch('sync.CONTENT',root),patch('sync.discover',return_value=[]),contextlib.redirect_stdout(io.StringIO()):
                sync.run(SimpleNamespace(full=True,pages=1,limit=1,delay=0,workers=1))
            state=core.read(root/'sync-state.json')
            self.assertEqual(state['sources'][u]['status'],'unsupported')
            self.assertEqual(state['pending'],0)
            self.assertEqual(state['unsupported'],1)

    def test_manual_import_respects_selected_professional_section(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);u='https://example.com/opinion';key=core.identity(u)
            core.write(root/'imports.json',{'imports':[{'url':u,'stream':'opinion','credit_type':'author-page','contribution':'Research','contribution_confirmed':True,'rights_confirmed':True,'status':'queued'}]})
            extracted={'id':key,'title':'An imported opinion','date_published':'2026-09-04T10:00:00+06:00','body_html':'<p>Text.</p>','category':'Commentary','source_url':u}
            with patch('sync.CONTENT',root),patch('sync.discover',return_value=[]),patch('sync.fetch',return_value=(b'<html></html>','text/html',u)),patch('sync.article',return_value=extracted.copy()),contextlib.redirect_stdout(io.StringIO()):
                sync.run(SimpleNamespace(full=True,pages=1,limit=1,delay=0,workers=1))
            saved=core.read(root/'articles'/f'{key}.json')
            self.assertEqual(saved['stream'],'opinion')
            self.assertEqual(saved['contribution'],'Research')
            self.assertEqual(saved['category'],'Commentary')
            self.assertEqual(saved['credit_type_override'],'author-page')

if __name__=='__main__':unittest.main()
