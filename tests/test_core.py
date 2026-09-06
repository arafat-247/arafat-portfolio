import copy, json, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import core, sync
from build import safe_asset, text_body

def sample(author=core.NAME, date='2026-09-05T12:00:00+06:00',body=None):
    obj={'@type':'NewsArticle','headline':'Testing public accountability','author':{'name':author},'datePublished':date,'articleBody':body or ('A substantive sentence about reporting and public accountability. '*15),'mainEntityOfPage':'https://example.com/news/story-12345'}
    return '<script type="application/ld+json">'+json.dumps(obj)+'</script>'

class ContentTests(unittest.TestCase):
    def test_exact_author(self):
        a=core.article(sample(),'https://example.com/news/story-12345')
        self.assertTrue(a['verified_author']);self.assertTrue(a['date_published']);self.assertGreater(a['word_count'],50)
    def test_non_author_rejected(self):
        with self.assertRaises(ValueError):core.article(sample('Someone Else'),'https://example.com/news/story-12345')
    def test_manual_retains_byline(self):
        a=core.article(sample('Staff Correspondent'),'https://example.com/news/story-12345',manual=True)
        self.assertEqual(a['original_authors'],['Staff Correspondent']);self.assertFalse(a['verified_author'])
    def test_sanitiser(self):
        out=core.sanitise('<script>bad()</script><p onclick="bad()">OK <a href="javascript:alert(1)">link</a><img src=x onerror=bad()></p><iframe>no</iframe>')
        self.assertNotIn('javascript',out);self.assertNotIn('onclick',out);self.assertNotIn('<script',out);self.assertNotIn('<img',out)
    def test_sanitiser_escaped_js(self):
        out=core.sanitise('<a href="java&#x73;cript:alert(1)">X</a>')
        self.assertNotIn('href',out)
    def test_private_urls(self):
        for u in ('http://example.com','https://localhost/foo','https://x.local','https://a:b@example.com/','https://example.com:8888'):
            with self.assertRaises(ValueError):core.public_url(u)
    def test_resolved_private_ip(self):
        with patch('core.socket.getaddrinfo',return_value=[(2,1,6,'',('127.0.0.1',443))]):
            with self.assertRaises(ValueError):core.public_url('https://example.com')
    def test_tracking_dedup(self):
        self.assertEqual(core.identity('https://example.com/a?utm_source=x'),core.identity('https://example.com/a'))
        self.assertNotEqual(core.identity('https://example.com/a?id=1'),core.identity('https://example.com/a?id=2'))
    def test_bad_asset(self):
        self.assertEqual(safe_asset('assets/../../secret'),'');self.assertEqual(safe_asset('https://x/a'),'')
    def test_text_escape(self):
        self.assertNotIn('<script>',text_body('<script>alert(1)</script>'))
    def test_missing_date(self):self.assertEqual(core.article(sample(date=''),'https://example.com/news/story-12345')['date_published'],'')
    def test_revision_and_short_extract(self):
        with tempfile.TemporaryDirectory() as d, patch('sync.CONTENT',Path(d)):
            a=core.article(sample(),'https://example.com/news/story-12345');a['status']='published';sync.store_article(a)
            old=json.loads((Path(d)/'articles'/f'{a["id"]}.json').read_text())
            b=copy.deepcopy(a);b['title']='Updated title';sync.store_article(b,old)
            self.assertEqual(len(list((Path(d)/'revisions').rglob('*.json'))),1)
            bad=copy.deepcopy(b);bad['word_count']=1;bad['body_html']='<p>Access denied</p>'
            with self.assertRaises(ValueError):sync.store_article(bad,b)
            saved=json.loads((Path(d)/'articles'/f'{a["id"]}.json').read_text());self.assertEqual(saved['title'],'Updated title')
    def test_drupal_body_and_date(self):
        source='<script type="application/ld+json">'+json.dumps({'@type':'NewsArticle','headline':'Example','author':{'name':core.NAME}})+'</script><article><span>5 September 2026</span><main><h2>Editor pick</h2><div class="node-content"><span>8 August 2026</span><div class="block-field-blocknodenewsbody"><p>'+('Actual reporting. '*40)+'</p></div></div></main></article>'
        a=core.article(source,'https://example.com/a');self.assertTrue(a['date_published'].startswith('2026-08-08'));self.assertNotIn('Editor pick',a['body_html'])
    def test_paywall(self):
        source=sample().replace('"@type": "NewsArticle"','"@type": "NewsArticle", "isAccessibleForFree": false')
        with self.assertRaises(ValueError):core.article(source,'https://example.com/news/story-12345')

if __name__=='__main__':unittest.main()
