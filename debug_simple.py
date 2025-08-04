#!/usr/bin/env python3

# Simple test script
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/src')

from markdown_blocks import markdown_to_blocks

md = """```python
def greet(name):
    return f"Hello, {name}!"

```"""

print("Markdown input:")
print(repr(md))
print()

blocks = markdown_to_blocks(md)
print("Blocks:")
for i, block in enumerate(blocks):
    print(f"Block {i}: {repr(block)}")
    lines = block.split('\n')
    print(f"  Lines: {lines}")
    if len(lines) > 2:
        print(f"  Content lines: {lines[1:-1]}")
        print(f"  Joined content: {repr(chr(10).join(lines[1:-1]))}")
