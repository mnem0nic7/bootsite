#!/usr/bin/env python3
import sys
sys.path.append('src')

from textnode import TextNode, TextType
from text_to_html import text_node_to_html_node

def demo_text_node_to_html_node():
    print("=== Demonstrating text_node_to_html_node function ===\n")
    
    # Test each TextType
    test_cases = [
        (TextNode("Plain text", TextType.TEXT), "TEXT"),
        (TextNode("Bold text", TextType.BOLD), "BOLD"),
        (TextNode("Italic text", TextType.ITALIC), "ITALIC"),
        (TextNode("console.log('hello')", TextType.CODE), "CODE"),
        (TextNode("Visit Boot.dev", TextType.LINK, "https://www.boot.dev"), "LINK"),
        (TextNode("A cool image", TextType.IMAGE, "https://example.com/cool.jpg"), "IMAGE"),
    ]
    
    for text_node, type_name in test_cases:
        html_node = text_node_to_html_node(text_node)
        html_output = html_node.to_html()
        print(f"{type_name:6}: {html_output}")

if __name__ == "__main__":
    demo_text_node_to_html_node()
