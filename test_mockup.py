from html.parser import HTMLParser
from pathlib import Path
import unittest


class MockupParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.options = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if element_id := attributes.get("id"):
            self.ids.add(element_id)
        if tag == "option":
            self.options.append(attributes.get("value"))

    def handle_data(self, data):
        if data.strip():
            self.text.append(data.strip())


class MockupContractTests(unittest.TestCase):
    def parse_mockup(self):
        parser = MockupParser()
        parser.feed(Path("mockup.html").read_text(encoding="utf-8"))
        return parser

    def test_mockup_uses_vietnamese_labels(self):
        parsed = self.parse_mockup()

        self.assertIn("Tutor thường", parsed.text)
        self.assertIn("Học viên", parsed.text)
        self.assertIn("Mở bằng chứng", parsed.text)
        self.assertNotIn("Tutor thuong", parsed.text)
        self.assertNotIn("Hoc vien", parsed.text)

    def test_mockup_offers_compatible_font_choices(self):
        parsed = self.parse_mockup()

        self.assertIn("font-select", parsed.ids)
        self.assertEqual(parsed.options, ["system", "sans", "serif", "mono"])
        self.assertIn("Hệ thống", parsed.text)
        self.assertIn("Sans-serif", parsed.text)
        self.assertIn("Serif", parsed.text)
        self.assertIn("Monospace", parsed.text)


if __name__ == "__main__":
    unittest.main()
