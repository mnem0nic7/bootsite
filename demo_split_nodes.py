#!/usr/bin/env python3
import sys
sys.path.append('src')

from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter

def demo_split_nodes_delimiter():
    print("=== Demonstrating split_nodes_delimiter function ===\n")
    
    # Example from the requirements
    print("1. Basic code delimiter example:")
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    for i, n in enumerate(new_nodes):
        print(f"   [{i}] {n}")
    print()
    
    # Multiple delimiters
    print("2. Multiple code blocks:")
    node = TextNode("This has `code` and `more code` in it", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    for i, n in enumerate(new_nodes):
        print(f"   [{i}] {n}")
    print()
    
    # Bold text
    print("3. Bold delimiter example:")
    node = TextNode("This text has **bold** words", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    for i, n in enumerate(new_nodes):
        print(f"   [{i}] {n}")
    print()
    
    # Chaining different delimiters
    print("4. Chaining different delimiters:")
    original = TextNode("Text with `code` and **bold** formatting", TextType.TEXT)
    print(f"   Original: {original}")
    
    # First handle code
    after_code = split_nodes_delimiter([original], "`", TextType.CODE)
    print("   After code processing:")
    for i, n in enumerate(after_code):
        print(f"     [{i}] {n}")
    
    # Then handle bold
    after_bold = split_nodes_delimiter(after_code, "**", TextType.BOLD)
    print("   After bold processing:")
    for i, n in enumerate(after_bold):
        print(f"     [{i}] {n}")
    print()
    
    # Mixed nodes (some already processed)
    print("5. Mixed node types (some already processed):")
    mixed_nodes = [
        TextNode("Regular text with `code`", TextType.TEXT),
        TextNode("Already bold text", TextType.BOLD),
        TextNode("More text with `another code`", TextType.TEXT),
    ]
    print("   Input nodes:")
    for i, n in enumerate(mixed_nodes):
        print(f"     [{i}] {n}")
    
    result = split_nodes_delimiter(mixed_nodes, "`", TextType.CODE)
    print("   After processing:")
    for i, n in enumerate(result):
        print(f"     [{i}] {n}")

if __name__ == "__main__":
    demo_split_nodes_delimiter()
