from htmlnode import HTMLNode, ParentNode, LeafNode
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from split_nodes import text_to_textnodes
from text_to_html import text_node_to_html_node


def text_to_children(text):
    """
    Convert inline markdown text to a list of HTMLNode children.
    
    Args:
        text: Raw text string that may contain inline markdown
    
    Returns:
        List of HTMLNode objects representing the inline elements
    """
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def heading_to_html_node(block):
    """Convert a heading block to an HTMLNode."""
    # Count the number of # characters
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break
    
    # Extract the heading text (skip the # characters and space)
    heading_text = block[level:].strip()
    children = text_to_children(heading_text)
    return ParentNode(f"h{level}", children)


def paragraph_to_html_node(block):
    """Convert a paragraph block to an HTMLNode."""
    # Replace newlines with spaces for paragraphs
    text = block.replace('\n', ' ')
    children = text_to_children(text)
    return ParentNode("p", children)


def code_to_html_node(block):
    """Convert a code block to an HTMLNode."""
    # Remove the opening and closing ``` and any language specifier
    lines = block.split('\n')
    # Remove first and last lines (the ``` lines)
    code_content = '\n'.join(lines[1:-1])
    
    # Code blocks don't process inline markdown
    code_node = LeafNode("code", code_content)
    return ParentNode("pre", [code_node])


def quote_to_html_node(block):
    """Convert a quote block to an HTMLNode."""
    lines = block.split('\n')
    # Remove the > character and space from each line
    quote_lines = []
    for line in lines:
        # Remove the '>' and any following space
        if line.startswith('> '):
            quote_lines.append(line[2:])
        elif line.startswith('>'):
            quote_lines.append(line[1:])
        else:
            quote_lines.append(line)
    
    quote_text = '\n'.join(quote_lines)
    children = text_to_children(quote_text)
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    """Convert an unordered list block to an HTMLNode."""
    lines = block.split('\n')
    list_items = []
    
    for line in lines:
        # Remove the '- ' from the beginning
        item_text = line[2:]  # Skip '- '
        item_children = text_to_children(item_text)
        list_item = ParentNode("li", item_children)
        list_items.append(list_item)
    
    return ParentNode("ul", list_items)


def ordered_list_to_html_node(block):
    """Convert an ordered list block to an HTMLNode."""
    lines = block.split('\n')
    list_items = []
    
    for line in lines:
        # Find the first '. ' and remove everything before it
        dot_index = line.find('. ')
        item_text = line[dot_index + 2:]  # Skip 'N. '
        item_children = text_to_children(item_text)
        list_item = ParentNode("li", item_children)
        list_items.append(list_item)
    
    return ParentNode("ol", list_items)


def markdown_to_html_node(markdown):
    """
    Convert a full markdown document into a single parent HTMLNode.
    
    Args:
        markdown: Raw markdown text string representing a full document
    
    Returns:
        HTMLNode representing the entire document as a div with child elements
    """
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.HEADING:
            node = heading_to_html_node(block)
        elif block_type == BlockType.PARAGRAPH:
            node = paragraph_to_html_node(block)
        elif block_type == BlockType.CODE:
            node = code_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            node = quote_to_html_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            node = unordered_list_to_html_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            node = ordered_list_to_html_node(block)
        else:
            # Default to paragraph
            node = paragraph_to_html_node(block)
        
        children.append(node)
    
    return ParentNode("div", children)
