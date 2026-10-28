"""Opt-in real-browser checks, with only an in-memory test page.

Run: python -m unittest discover -s tests -p test_browser.py -v
If Chromium is not installed these checks are explicitly skipped.
"""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from automation import Tools
from core import Declined

HTML = """<!doctype html><html lang="bn"><body>
<h1>পরীক্ষার পাতা</h1><label>নির্দেশ<input id="instruction"></label>
<input type="password" aria-label="Secret password" value="DO_NOT_READ_THIS">
<input type="hidden" value="HIDDEN_VALUE">
<label>Language<select><option>English</option><option>বাংলা</option></select></label>
<button onclick="document.getElementById('result').textContent='সম্পন্ন'">শুরু করুন</button>
<p id="result">প্রস্তুত</p></body></html>"""


class BrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            from playwright.sync_api import sync_playwright
            cls.engine = sync_playwright().start()
            cls.browser = cls.engine.chromium.launch(headless=True)
        except Exception as exc:
            if getattr(cls, "engine", None):
                cls.engine.stop()
            raise unittest.SkipTest(f"Chromium is not installed: {exc}")

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.engine.stop()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.set_content(HTML)
        self.tools = Tools(Path(self.tmp.name), Path(self.tmp.name), {}, lambda *args: True, lambda *args: None)
        self.tools.context, self.tools.page = self.context, self.page

    def tearDown(self):
        self.context.close()
        self.tmp.cleanup()

    def test_bangla_read_and_password_exclusion(self):
        data = self.tools.browser_read()
        self.assertIn("পরীক্ষার পাতা", data["text"])
        self.assertNotIn("DO_NOT_READ_THIS", str(data))
        self.assertNotIn("Secret password", str(data))
        self.assertNotIn("HIDDEN_VALUE", str(data))

    def test_fill_unicode_and_invalidate_control_id(self):
        data = self.tools.browser_read()
        control = next(c for c in data["controls"] if c["tag"] == "input")
        self.tools.browser_fill(control["id"], "আমার নির্দেশ")
        self.assertEqual(self.page.locator("#instruction").input_value(), "আমার নির্দেশ")
        with self.assertRaisesRegex(ValueError, "stale"):
            self.tools.browser_fill(control["id"], "Must not happen")

    def test_click_has_observable_effect(self):
        data = self.tools.browser_read()
        control = next(c for c in data["controls"] if c["tag"] == "button")
        self.tools.browser_click(control["id"])
        self.assertEqual(self.page.locator("#result").inner_text(), "সম্পন্ন")

    def test_decline_click_leaves_page_unchanged(self):
        data = self.tools.browser_read()
        control = next(c for c in data["controls"] if c["tag"] == "button")
        self.tools.approve = lambda *args: False
        with self.assertRaises(Declined):
            self.tools.browser_click(control["id"])
        self.assertEqual(self.page.locator("#result").inner_text(), "প্রস্তুত")

    def test_select_option_by_bangla_label(self):
        data = self.tools.browser_read()
        control = next(c for c in data["controls"] if c["tag"] == "select")
        self.tools.browser_select(control["id"], "বাংলা")
        self.assertEqual(self.page.locator("select").input_value(), "বাংলা")

    def test_tabs_switch_and_stale_id(self):
        data = self.tools.browser_read()
        control = next(c for c in data["controls"] if c["tag"] == "input")
        new_page = self.context.new_page()
        new_page.set_content("<body>Second tab</body>")
        self.assertEqual(len(self.tools.browser_tabs()), 2)
        self.tools.browser_switch(1)
        self.assertEqual(self.tools.browser_read()["text"], "Second tab")
        with self.assertRaises(ValueError):
            self.tools.browser_fill(control["id"], "No")


if __name__ == "__main__":
    unittest.main()
