import unittest

from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        md = "This is just a single paragraph with some text."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is just a single paragraph with some text."])

    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_whitespace(self):
        md = "   \n\n   \t\t  \n\n  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_excessive_newlines(self):
        md = """
First paragraph


Second paragraph



Third paragraph


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First paragraph",
                "Second paragraph",
                "Third paragraph",
            ],
        )

    def test_markdown_to_blocks_with_heading(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_markdown_to_blocks_code_block(self):
        md = """Here's some code:

```python
def hello():
    print("Hello, world!")
```

And here's more text."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Here's some code:",
                "```python\ndef hello():\n    print(\"Hello, world!\")\n```",
                "And here's more text.",
            ],
        )

    def test_markdown_to_blocks_mixed_content(self):
        md = """# Main Title

## Subtitle

This is a paragraph with **bold** text.

> This is a blockquote
> that spans multiple lines

1. Ordered list item
2. Another item

- Unordered list
- Another item

Final paragraph."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Main Title",
                "## Subtitle",
                "This is a paragraph with **bold** text.",
                "> This is a blockquote\n> that spans multiple lines",
                "1. Ordered list item\n2. Another item",
                "- Unordered list\n- Another item",
                "Final paragraph.",
            ],
        )

    def test_markdown_to_blocks_leading_trailing_whitespace(self):
        md = """   

  First block with spaces  

  
  Second block with tabs	

	
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block with spaces",
                "Second block with tabs",
            ],
        )

    def test_markdown_to_blocks_single_newlines_preserved(self):
        md = """This is line one
This is line two

This is a new block
With another line"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is line one\nThis is line two",
                "This is a new block\nWith another line",
            ],
        )

    def test_markdown_to_blocks_many_empty_blocks(self):
        md = "Block 1\n\n\n\n\n\nBlock 2\n\n\n\nBlock 3"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2", "Block 3"])


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_heading_h1(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_h2(self):
        block = "## This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_h6(self):
        block = "###### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_invalid_no_space(self):
        block = "#This is not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_heading_invalid_too_many_hashes(self):
        block = "####### This is not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_code_block(self):
        block = "```\nprint('hello')\nprint('world')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_code_block_single_line(self):
        block = "```code```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_code_block_with_language(self):
        block = "```python\ndef hello():\n    print('Hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_code_block_invalid_no_closing(self):
        block = "```python\ncode here"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote_single_line(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_quote_multi_line(self):
        block = "> This is a quote\n> that spans multiple lines\n> and continues here"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_quote_invalid_missing_marker(self):
        block = "> This is a quote\nThis line doesn't have a marker"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list_single_item(self):
        block = "- This is a list item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_multiple_items(self):
        block = "- First item\n- Second item\n- Third item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_invalid_no_space(self):
        block = "-No space after dash"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list_invalid_missing_dash(self):
        block = "- First item\nSecond item without dash"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_single_item(self):
        block = "1. This is an ordered list item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_multiple_items(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_invalid_wrong_number(self):
        block = "1. First item\n3. Wrong number"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_invalid_starts_wrong(self):
        block = "2. Starts with wrong number"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_invalid_no_space(self):
        block = "1.No space after period"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_plain_text(self):
        block = "This is just a regular paragraph with some text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_multi_line(self):
        block = "This is a paragraph\nthat spans multiple lines\nbut is still a paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_with_formatting(self):
        block = "This paragraph has **bold** and *italic* text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_heading_edge_cases(self):
        # Test exact boundary cases for headings
        valid_headings = [
            "# H1",
            "## H2", 
            "### H3",
            "#### H4",
            "##### H5",
            "###### H6"
        ]
        
        for heading in valid_headings:
            with self.subTest(heading=heading):
                self.assertEqual(block_to_block_type(heading), BlockType.HEADING)

    def test_block_to_block_type_ordered_list_long_sequence(self):
        block = "1. Item one\n2. Item two\n3. Item three\n4. Item four\n5. Item five"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_quote_with_nested_formatting(self):
        block = "> This quote has **bold** text\n> And *italic* text too\n> Even `code` snippets"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_empty_string(self):
        # Although this shouldn't happen due to our filtering, test edge case
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
