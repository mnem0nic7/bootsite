import unittest

from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_bold_delimiter(self):
        node = TextNode("This is text with **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_italic_delimiter(self):
        node = TextNode("This is text with *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_multiple_delimiters(self):
        node = TextNode("This has `code` and `more code` in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_no_delimiter(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("This is plain text", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_split_delimiter_at_start(self):
        node = TextNode("`code` at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" at the start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_delimiter_at_end(self):
        node = TextNode("Text with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_only_delimited_text(self):
        node = TextNode("`only code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("only code", TextType.CODE)]
        self.assertEqual(new_nodes, expected)

    def test_non_text_nodes_unchanged(self):
        nodes = [
            TextNode("Regular text with `code`", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Already italic", TextType.ITALIC),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("Regular text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Already italic", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected)

    def test_unmatched_delimiter_raises_error(self):
        node = TextNode("This has unmatched `delimiter", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertIn("unmatched delimiter", str(context.exception))

    def test_multiple_unmatched_delimiters_raises_error(self):
        node = TextNode("This `has` unmatched `delimiters here", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertIn("unmatched delimiter", str(context.exception))

    def test_empty_delimited_text(self):
        node = TextNode("Text with `` empty code", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode(" empty code", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_nodes_input(self):
        nodes = [
            TextNode("First `code` block", TextType.TEXT),
            TextNode("Second `code` block", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block", TextType.TEXT),
            TextNode("Second ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_chaining_different_delimiters(self):
        # Test that we can chain different delimiter operations
        node = TextNode("Text with `code` and **bold** formatting", TextType.TEXT)
        
        # First split by code delimiters
        nodes_after_code = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_after_code = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and **bold** formatting", TextType.TEXT),
        ]
        self.assertEqual(nodes_after_code, expected_after_code)
        
        # Then split by bold delimiters
        nodes_after_bold = split_nodes_delimiter(nodes_after_code, "**", TextType.BOLD)
        expected_final = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" formatting", TextType.TEXT),
        ]
        self.assertEqual(nodes_after_bold, expected_final)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_images_no_images(self):
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [node])

    def test_split_images_image_at_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) at the start",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" at the start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_images_image_at_end(self):
        node = TextNode(
            "Text with ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_images_only_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_images_empty_alt_text(self):
        node = TextNode(
            "Image with ![](https://i.imgur.com/zjjcJKZ.png) empty alt",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Image with ", TextType.TEXT),
            TextNode("", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" empty alt", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_images_non_text_nodes_unchanged(self):
        nodes = [
            TextNode("Text with ![image](https://example.com/img.jpg)", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Already italic", TextType.ITALIC),
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.jpg"),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Already italic", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_images_multiple_nodes_input(self):
        nodes = [
            TextNode("First ![img1](https://example.com/1.jpg) node", TextType.TEXT),
            TextNode("Second ![img2](https://example.com/2.jpg) node", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "https://example.com/1.jpg"),
            TextNode(" node", TextType.TEXT),
            TextNode("Second ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "https://example.com/2.jpg"),
            TextNode(" node", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_links_single_link(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.example.com"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_links_no_links(self):
        node = TextNode("This is text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])

    def test_split_links_link_at_start(self):
        node = TextNode(
            "[link](https://www.example.com) at the start",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("link", TextType.LINK, "https://www.example.com"),
            TextNode(" at the start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_links_link_at_end(self):
        node = TextNode(
            "Text with [link](https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.example.com"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_links_only_link(self):
        node = TextNode(
            "[link](https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("link", TextType.LINK, "https://www.example.com"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_links_empty_anchor_text(self):
        node = TextNode(
            "Link with [](https://www.example.com) empty text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Link with ", TextType.TEXT),
            TextNode("", TextType.LINK, "https://www.example.com"),
            TextNode(" empty text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_links_non_text_nodes_unchanged(self):
        nodes = [
            TextNode("Text with [link](https://example.com)", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Already italic", TextType.ITALIC),
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Already italic", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_links_multiple_nodes_input(self):
        nodes = [
            TextNode("First [link1](https://example.com/1) node", TextType.TEXT),
            TextNode("Second [link2](https://example.com/2) node", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "https://example.com/1"),
            TextNode(" node", TextType.TEXT),
            TextNode("Second ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "https://example.com/2"),
            TextNode(" node", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_links_ignores_images(self):
        # Links should not extract images (which start with !)
        node = TextNode(
            "Text with ![image](https://example.com/img.jpg) and [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Text with ![image](https://example.com/img.jpg) and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_links_complex_urls(self):
        node = TextNode(
            "Complex [search](https://www.google.com/search?q=python&oq=python) URL",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Complex ", TextType.TEXT),
            TextNode("search", TextType.LINK, "https://www.google.com/search?q=python&oq=python"),
            TextNode(" URL", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)


class TestSplitNodesIntegration(unittest.TestCase):
    def test_chaining_image_and_link_splitting(self):
        # Test that we can chain image and link splitting
        node = TextNode(
            "Text with ![image](https://example.com/img.jpg) and [link](https://example.com)",
            TextType.TEXT,
        )
        
        # First split images
        nodes_after_images = split_nodes_image([node])
        expected_after_images = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.jpg"),
            TextNode(" and [link](https://example.com)", TextType.TEXT),
        ]
        self.assertEqual(nodes_after_images, expected_after_images)
        
        # Then split links
        nodes_after_links = split_nodes_link(nodes_after_images)
        expected_final = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.jpg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(nodes_after_links, expected_final)


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_full_example(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_plain_text(self):
        text = "This is just plain text with no formatting"
        nodes = text_to_textnodes(text)
        expected = [TextNode("This is just plain text with no formatting", TextType.TEXT)]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_only_bold(self):
        text = "This has **bold** text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_only_italic(self):
        text = "This has *italic* text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_only_code(self):
        text = "This has `code` text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_only_image(self):
        text = "This has ![image](https://example.com/img.jpg) only"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.jpg"),
            TextNode(" only", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_only_link(self):
        text = "This has [link](https://example.com) only"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" only", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_multiple_same_type(self):
        text = "Multiple **bold** and **more bold** words"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Multiple ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("more bold", TextType.BOLD),
            TextNode(" words", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_nested_formatting_order(self):
        # Test that the order of operations matters
        text = "Text with **bold and *italic* inside**"
        nodes = text_to_textnodes(text)
        # Should first split by **, then by *, so the bold contains the italic delimiter
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("bold and *italic* inside", TextType.BOLD),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_complex_mix(self):
        text = "Start **bold** then *italic* and `code` with ![img](https://example.com/img.jpg) and [link](https://example.com) end"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" then ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" with ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "https://example.com/img.jpg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_empty_string(self):
        text = ""
        nodes = text_to_textnodes(text)
        # Empty strings get filtered out by our splitting functions
        expected = []
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_consecutive_formatting(self):
        text = "**bold***italic*`code`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_image_and_link_together(self):
        text = "![image](https://example.com/img.jpg)[link](https://example.com)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("image", TextType.IMAGE, "https://example.com/img.jpg"),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(nodes, expected)


if __name__ == "__main__":
    unittest.main()
