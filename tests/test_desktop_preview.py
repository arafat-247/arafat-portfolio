import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_desktop_preview


class DesktopPreviewIsolationTests(unittest.TestCase):
    def test_replaces_only_complete_desktop_section(self):
        source = (
            '<main>'
            '<section class="deskhome live"><div><section class="nested">keep inside source only</section></div></section>'
            '<section class="portalhome portalhome-mobile">MOBILE-CANARY</section>'
            '</main>'
        )
        result = build_desktop_preview.replace_desk_section(
            source,
            '<section class="deskhome preview">PREVIEW-ONLY</section>',
        )
        self.assertIn('class="deskhome preview"', result)
        self.assertNotIn('keep inside source only', result)
        self.assertIn('MOBILE-CANARY', result)
        self.assertEqual(result.count('class="deskhome'), 1)


    def test_shared_desk_markup_is_live_safe(self):
        self.assertNotIn('href="desktop-preview/', build_desktop_preview.DESK)
        self.assertIn('href="./"', build_desktop_preview.DESK)
        self.assertIn('<a href="all-work/">Work</a>', build_desktop_preview.DESK)
        self.assertIn('class="button" href="#work"', build_desktop_preview.DESK)
        self.assertIn('href="contact/"', build_desktop_preview.DESK)
        self.assertIn('class="clock-surface desktop-clock"', build_desktop_preview.DESK)
        self.assertIn('class="category-grid"', build_desktop_preview.DESK)
        self.assertNotIn('href="#contact"', build_desktop_preview.DESK)


if __name__ == "__main__":
    unittest.main()
