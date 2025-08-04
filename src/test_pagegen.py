import unittest
from pagegen import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(extract_title("# Hello"), "Hello")
    def test_leading_trailing_whitespace(self):
        self.assertEqual(extract_title("   #   Hello world   "), "Hello world")
    def test_multiline(self):
        md = """
foo
# My Title
bar
"""
        self.assertEqual(extract_title(md), "My Title")
    def test_no_h1(self):
        with self.assertRaises(Exception):
            extract_title("## Not a title\nNo h1 here")
    def test_h1_not_at_start(self):
        md = "foo\n# Title\nbar"
        self.assertEqual(extract_title(md), "Title")
    def test_h1_with_extra_hashes(self):
        self.assertEqual(extract_title("# Title #"), "Title #")

if __name__ == "__main__":
    unittest.main()
