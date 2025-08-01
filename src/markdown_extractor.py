import re


def extract_markdown_images(text):
    """
    Extract markdown images from text.
    
    Args:
        text: Raw markdown text string
        
    Returns:
        List of tuples containing (alt_text, url) for each image found
    """
    # Regex pattern for markdown images: ![alt text](url)
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    """
    Extract markdown links from text (excluding images).
    
    Args:
        text: Raw markdown text string
        
    Returns:
        List of tuples containing (anchor_text, url) for each link found
    """
    # Regex pattern for markdown links: [anchor text](url)
    # Uses negative lookbehind (?<!) to exclude images (which start with !)
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches
