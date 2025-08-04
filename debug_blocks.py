#!/usr/bin/env python3

import sys
import os
sys.path.append('/home/gallison/workspace/bootsite1/src')

from markdown_blocks import markdown_to_blocks

md1 = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

md2 = """This is a paragraph
that spans multiple lines
but should still be one paragraph."""

print('Test 1 markdown:')
print(repr(md1))
print('Test 1 blocks:')
blocks1 = markdown_to_blocks(md1)
for i, block in enumerate(blocks1):
    print(f'  Block {i}: {repr(block)}')

print()
print('Test 2 markdown:')
print(repr(md2))
print('Test 2 blocks:')
blocks2 = markdown_to_blocks(md2)
for i, block in enumerate(blocks2):
    print(f'  Block {i}: {repr(block)}')
