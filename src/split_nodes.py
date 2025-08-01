from textnode import TextNode, TextType
from markdown_extractor import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split text nodes by delimiter and convert delimited text to specified text_type.
    
    Args:
        old_nodes: List of TextNode objects
        delimiter: String delimiter to split on (e.g., "`", "**", "_")
        text_type: TextType to assign to delimited text
    
    Returns:
        List of TextNode objects with delimited text converted to specified type
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Only split TEXT type nodes, leave others as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Split the text by the delimiter
        split_text = old_node.text.split(delimiter)
        
        # Check if we have an even number of parts (valid delimiter pairs)
        if len(split_text) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax: unmatched delimiter '{delimiter}'")
        
        # Process the split parts
        for i, part in enumerate(split_text):
            if part == "":
                # Skip empty parts (happens when delimiter is at start/end)
                continue
            
            if i % 2 == 0:
                # Even indices are regular text
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # Odd indices are delimited text (convert to specified type)
                new_nodes.append(TextNode(part, text_type))
    
    return new_nodes


def split_nodes_image(old_nodes):
    """
    Split text nodes containing markdown images into separate nodes.
    
    Args:
        old_nodes: List of TextNode objects
    
    Returns:
        List of TextNode objects with images converted to IMAGE type nodes
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Only split TEXT type nodes, leave others as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        current_text = old_node.text
        images = extract_markdown_images(current_text)
        
        # If no images found, add the original node
        if not images:
            new_nodes.append(old_node)
            continue
        
        # Process each image found
        for image_alt, image_url in images:
            # Split on the current image markdown
            image_markdown = f"![{image_alt}]({image_url})"
            sections = current_text.split(image_markdown, 1)
            
            # Add text before the image (if not empty)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            # Add the image node
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            
            # Continue with the remaining text
            current_text = sections[1] if len(sections) > 1 else ""
        
        # Add any remaining text after the last image (if not empty)
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return new_nodes


def split_nodes_link(old_nodes):
    """
    Split text nodes containing markdown links into separate nodes.
    
    Args:
        old_nodes: List of TextNode objects
    
    Returns:
        List of TextNode objects with links converted to LINK type nodes
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Only split TEXT type nodes, leave others as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        current_text = old_node.text
        links = extract_markdown_links(current_text)
        
        # If no links found, add the original node
        if not links:
            new_nodes.append(old_node)
            continue
        
        # Process each link found
        for link_text, link_url in links:
            # Split on the current link markdown
            link_markdown = f"[{link_text}]({link_url})"
            sections = current_text.split(link_markdown, 1)
            
            # Add text before the link (if not empty)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            # Add the link node
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            
            # Continue with the remaining text
            current_text = sections[1] if len(sections) > 1 else ""
        
        # Add any remaining text after the last link (if not empty)
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return new_nodes


def text_to_textnodes(text):
    """
    Convert a raw markdown text string into a list of TextNode objects.
    
    This function applies all the splitting operations in sequence:
    1. Split by bold delimiters (**)
    2. Split by italic delimiters (*)
    3. Split by code delimiters (`)
    4. Split by images
    5. Split by links
    
    Args:
        text: Raw markdown text string
    
    Returns:
        List of TextNode objects representing the parsed markdown
    """
    # Start with a single TEXT node containing the entire text
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Apply all splitting operations in sequence
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)  # Handle underscore italic
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes
