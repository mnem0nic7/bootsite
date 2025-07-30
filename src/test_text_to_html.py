import unittest

from textnode import TextNode, TextType
from text_to_html import text_node_to_html_node


class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
        self.assertIsNone(html_node.props)

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")
        self.assertIsNone(html_node.props)

    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")
        self.assertIsNone(html_node.props)

    def test_link(self):
        node = TextNode("Click me!", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image(self):
        node = TextNode("An image", TextType.IMAGE, "https://example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.jpg", "alt": "An image"})

    def test_invalid_text_type(self):
        # Create a text node with an invalid enum (this is tricky to test)
        # We'll test by creating a custom invalid type
        class InvalidTextType:
            def __init__(self, value):
                self.value = value
        
        invalid_node = TextNode("Invalid", InvalidTextType("invalid"))
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(invalid_node)
        self.assertIn("Invalid text type", str(context.exception))

    def test_to_html_integration(self):
        # Test that the returned LeafNode can actually render HTML
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_link_to_html_integration(self):
        # Test link rendering
        node = TextNode("Visit Google", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<a href="https://www.google.com">Visit Google</a>')

    def test_image_to_html_integration(self):
        # Test image rendering
        node = TextNode("A beautiful sunset", TextType.IMAGE, "sunset.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<img src="sunset.jpg" alt="A beautiful sunset"></img>')


if __name__ == "__main__":
    unittest.main()
