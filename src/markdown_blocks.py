from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    """
    Split a raw markdown string into blocks based on double newlines.
    
    Args:
        markdown: Raw markdown text string representing a full document
    
    Returns:
        List of block strings with leading/trailing whitespace stripped
        and empty blocks removed
    """
    # Split on double newlines to separate blocks
    blocks = markdown.split('\n\n')
    
    # Strip whitespace and filter out empty blocks
    filtered_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:  # Only add non-empty blocks
            filtered_blocks.append(stripped_block)
    
    return filtered_blocks


def block_to_block_type(block):
    """
    Determine the type of a markdown block.
    
    Args:
        block: A single block of markdown text (already stripped of leading/trailing whitespace)
    
    Returns:
        BlockType enum representing the type of block
    """
    lines = block.split('\n')
    
    # Check for heading (1-6 # characters followed by space)
    if block.startswith(('#', '##', '###', '####', '#####', '######')):
        # Must have space after the # characters
        heading_match = block.split(' ', 1)
        if len(heading_match) > 1 and all(c == '#' for c in heading_match[0]) and 1 <= len(heading_match[0]) <= 6:
            return BlockType.HEADING
    
    # Check for code block (starts and ends with 3 backticks)
    if block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    
    # Check for quote block (every line starts with >)
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    
    # Check for unordered list (every line starts with - followed by space)
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    
    # Check for ordered list (every line starts with number. followed by space, starting at 1)
    is_ordered_list = True
    for i, line in enumerate(lines):
        expected_number = i + 1
        expected_prefix = f"{expected_number}. "
        if not line.startswith(expected_prefix):
            is_ordered_list = False
            break
    
    if is_ordered_list and len(lines) > 0:
        return BlockType.ORDERED_LIST
    
    # Default to paragraph
    return BlockType.PARAGRAPH
