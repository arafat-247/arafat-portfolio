import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import polish_footer


class FooterPolishTests(unittest.TestCase):
    def test_homepage_preserves_reference_desk_footer(self):
        source = (
            '<section class="deskhome desk"><footer class="desk-signoff">DESK-CANARY</footer></section>'
            '<section class="portalhome portalhome-mobile"><footer class="portalfooter">MOBILE-CANARY</footer></section>'
            '<footer>OUTER-CANARY</footer>'
        )
        shared = '<footer class="sitefooter">SHARED-CANARY</footer>'
        result = polish_footer.replace_page_footer(source, shared, homepage=True)
        self.assertIn('<footer class="desk-signoff">DESK-CANARY</footer>', result)
        self.assertNotIn('MOBILE-CANARY', result)
        self.assertIn('<section class="portalhome portalhome-mobile"><footer class="sitefooter">SHARED-CANARY</footer></section>', result)
        self.assertIn('<footer>OUTER-CANARY</footer>', result)

    def test_inner_page_still_replaces_first_footer(self):
        source = '<main>BODY</main><footer>OLD</footer>'
        shared = '<footer class="sitefooter">NEW</footer>'
        result = polish_footer.replace_page_footer(source, shared)
        self.assertNotIn('<footer>OLD</footer>', result)
        self.assertIn('<footer class="sitefooter">NEW</footer>', result)


if __name__ == "__main__":
    unittest.main()
