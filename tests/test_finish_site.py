import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import finish_site  # noqa: E402


class CropPublisherStripTest(unittest.TestCase):
    def test_crops_navy_strip_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cover.jpg"
            image = Image.new("RGB", (754, 425), (200, 180, 150))
            image.paste((11, 32, 99), (0, 382, 754, 425))
            image.paste((255, 255, 255), (650, 395, 740, 415))  # logo on the right
            image.save(path, "JPEG", quality=95)
            self.assertTrue(finish_site.crop_publisher_strip(path))
            with Image.open(path) as cropped:
                self.assertLessEqual(cropped.size[1], 382)
                self.assertGreater(cropped.size[1], 370)
            self.assertFalse(finish_site.crop_publisher_strip(path))

    def test_leaves_ordinary_photographs_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "photo.jpg"
            Image.new("RGB", (800, 600), (120, 140, 90)).save(path, "JPEG")
            self.assertFalse(finish_site.crop_publisher_strip(path))


class PrivateLinksTest(unittest.TestCase):
    def test_links_to_private_pages_are_removed(self):
        source = '<nav><a href="../newsroom/">Reporting desk</a><a href="../about/">About</a><a href="/assistant/">App</a></nav>'
        cleaned = finish_site.LINK_TO_PRIVATE.sub("", source)
        self.assertEqual(cleaned, '<nav><a href="../about/">About</a></nav>')


if __name__ == "__main__":
    unittest.main()
