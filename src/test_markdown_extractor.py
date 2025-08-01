import unittest

from markdown_extractor import extract_markdown_images, extract_markdown_links


class TestMarkdownExtractor(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_images_no_images(self):
        text = "This is text with no images, just regular text"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_images_empty_alt_text(self):
        text = "This has an image with empty alt text ![](https://i.imgur.com/test.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("", "https://i.imgur.com/test.png")], matches)

    def test_extract_markdown_images_complex_alt_text(self):
        text = "This has ![complex alt text with spaces and numbers 123](https://example.com/image.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("complex alt text with spaces and numbers 123", "https://example.com/image.jpg")], matches)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_links_single_link(self):
        text = "Check out this [awesome website](https://www.example.com)!"
        matches = extract_markdown_links(text)
        self.assertListEqual([("awesome website", "https://www.example.com")], matches)

    def test_extract_markdown_links_no_links(self):
        text = "This is just plain text with no links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_empty_anchor_text(self):
        text = "This has a link with empty anchor text [](https://www.example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("", "https://www.example.com")], matches)

    def test_extract_markdown_links_excludes_images(self):
        text = "This has an ![image](https://example.com/img.jpg) and a [link](https://example.com)"
        matches = extract_markdown_links(text)
        # Should only return the link, not the image
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_markdown_images_excludes_links(self):
        text = "This has a [link](https://example.com) and an ![image](https://example.com/img.jpg)"
        matches = extract_markdown_images(text)
        # Should only return the image, not the link
        self.assertListEqual([("image", "https://example.com/img.jpg")], matches)

    def test_mixed_content_both_functions(self):
        text = "Mixed content with ![image1](https://img1.com) and [link1](https://link1.com) and ![image2](https://img2.com) and [link2](https://link2.com)"
        
        image_matches = extract_markdown_images(text)
        expected_images = [
            ("image1", "https://img1.com"),
            ("image2", "https://img2.com")
        ]
        self.assertListEqual(expected_images, image_matches)
        
        link_matches = extract_markdown_links(text)
        expected_links = [
            ("link1", "https://link1.com"),
            ("link2", "https://link2.com")
        ]
        self.assertListEqual(expected_links, link_matches)

    def test_complex_urls(self):
        text = "Complex URLs: [Google Search](https://www.google.com/search?q=python&oq=python) and ![Logo](https://cdn.example.com/assets/logo.png?v=1.2.3)"
        
        link_matches = extract_markdown_links(text)
        self.assertListEqual([("Google Search", "https://www.google.com/search?q=python&oq=python")], link_matches)
        
        image_matches = extract_markdown_images(text)
        self.assertListEqual([("Logo", "https://cdn.example.com/assets/logo.png?v=1.2.3")], image_matches)

    def test_nested_brackets_protection(self):
        # The regex should not match nested brackets
        text = "This should not match [outer [inner] text](https://example.com)"
        matches = extract_markdown_links(text)
        # Should not match because of nested brackets in anchor text
        self.assertListEqual([], matches)

    def test_nested_parentheses_protection(self):
        # The regex should not match nested parentheses
        text = "This should not match [text](https://example.com/path(with)parens)"
        matches = extract_markdown_links(text)
        # Should not match because of nested parentheses in URL
        self.assertListEqual([], matches)

    def test_relative_paths(self):
        text = "Relative paths: [local link](./local/path.html) and ![local image](../images/pic.jpg)"
        
        link_matches = extract_markdown_links(text)
        self.assertListEqual([("local link", "./local/path.html")], link_matches)
        
        image_matches = extract_markdown_images(text)
        self.assertListEqual([("local image", "../images/pic.jpg")], image_matches)


if __name__ == "__main__":
    unittest.main()
