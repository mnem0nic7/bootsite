import unittest

from markdown_to_html import markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_single_paragraph(self):
        md = "This is a simple paragraph with no formatting."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a simple paragraph with no formatting.</p></div>",
        )

    def test_heading_all_levels(self):
        md = """# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>"
        self.assertEqual(html, expected)

    def test_heading_with_formatting(self):
        md = "# This is a **bold** heading with *italic* text"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a <b>bold</b> heading with <i>italic</i> text</h1></div>",
        )

    def test_unordered_list(self):
        md = """- First item
- Second item with **bold** text
- Third item with [link](https://example.com)"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = '<div><ul><li>First item</li><li>Second item with <b>bold</b> text</li><li>Third item with <a href="https://example.com">link</a></li></ul></div>'
        self.assertEqual(html, expected)

    def test_ordered_list(self):
        md = """1. First item
2. Second item with *italic* text
3. Third item with `code`"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = '<div><ol><li>First item</li><li>Second item with <i>italic</i> text</li><li>Third item with <code>code</code></li></ol></div>'
        self.assertEqual(html, expected)

    def test_quote_block(self):
        md = """> This is a quote
> that spans multiple lines
> and has some **bold** text"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = '<div><blockquote>This is a quote\nthat spans multiple lines\nand has some <b>bold</b> text</blockquote></div>'
        self.assertEqual(html, expected)

    def test_mixed_content(self):
        md = """# Main Title

This is a paragraph with **bold** text.

- List item 1
- List item 2

> This is a quote

```
def hello():
    print("Hello, world!")
```

Another paragraph at the end."""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = '<div><h1>Main Title</h1><p>This is a paragraph with <b>bold</b> text.</p><ul><li>List item 1</li><li>List item 2</li></ul><blockquote>This is a quote</blockquote><pre><code>def hello():\n    print("Hello, world!")</code></pre><p>Another paragraph at the end.</p></div>'
        self.assertEqual(html, expected)

    def test_code_block_with_language(self):
        md = """```python
def greet(name):
    return f"Hello, {name}!"
```"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = '<div><pre><code>def greet(name):\n    return f"Hello, {name}!"</code></pre></div>'
        self.assertEqual(html, expected)

    def test_empty_markdown(self):
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    def test_whitespace_only(self):
        md = "   \n\n   "
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    def test_complex_inline_formatting(self):
        md = "This paragraph has **bold**, *italic*, `code`, ![image](https://example.com/img.jpg), and [link](https://example.com) elements."
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = '<div><p>This paragraph has <b>bold</b>, <i>italic</i>, <code>code</code>, <img src="https://example.com/img.jpg" alt="image"></img>, and <a href="https://example.com">link</a> elements.</p></div>'
        self.assertEqual(html, expected)

    def test_single_quote_line(self):
        md = "> Single line quote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>Single line quote</blockquote></div>")

    def test_single_list_item(self):
        md = "- Single list item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>Single list item</li></ul></div>")

    def test_single_ordered_item(self):
        md = "1. Single ordered item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>Single ordered item</li></ol></div>")

    def test_paragraph_with_line_breaks(self):
        md = """This is a paragraph
that spans multiple lines
but should still be one paragraph."""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><p>This is a paragraph that spans multiple lines but should still be one paragraph.</p></div>"
        self.assertEqual(html, expected)


if __name__ == "__main__":
    unittest.main()
