#!/usr/bin/env python3

from src.markdown_blocks import markdown_to_blocks
from src.markdown_to_html import markdown_to_html_node

md = """```python
def greet(name):
    return f"Hello, {name}!"
```"""

print('Raw markdown:')
print(repr(md))
print()

blocks = markdown_to_blocks(md)
print('Blocks:')
for i, block in enumerate(blocks):
    print(f'Block {i}: {repr(block)}')
print()

node = markdown_to_html_node(md)
html = node.to_html()
print('Generated HTML:')
print(repr(html))
print()

expected = '<div><pre><code>def greet(name):\n    return f"Hello, {name}!"\n</code></pre></div>'
print('Expected HTML:')
print(repr(expected))
print()

print('Match?', html == expected)
