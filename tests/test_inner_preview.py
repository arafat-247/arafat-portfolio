import unittest
from scripts import build_inner_preview

SAMPLE = '''<!doctype html><html><head><title>Old</title></head><body class="inner" data-root="../"><aside class="identity"></aside><div class="right"><main><section class="page"></section></main></div></body></html>'''

class InnerPreviewTests(unittest.TestCase):
    def test_decorate_adds_prototype_shell_only(self):
        out = build_inner_preview.decorate(SAMPLE, "reporting", "Reports & Features")
        self.assertIn('class="inner inner-prototype"', out)
        self.assertIn('class="prototype-head"', out)
        self.assertIn('Desktop inner-page prototype', out)
        self.assertIn('noindex,nofollow', out)
        self.assertIn('<base href="/">', out)
        self.assertIn('Prototype — Reports & Features', out)

    def test_first_story_path_uses_archive_link(self):
        source = '<a href="../stories/example-story/">Story</a>'
        path = build_inner_preview.first_story_path(source)
        self.assertTrue(str(path).endswith('dist/stories/example-story/index.html'))

if __name__ == "__main__":
    unittest.main()
