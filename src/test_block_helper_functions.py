import unittest
from blocknode import *
from block_helper_functions import *

class TestBlockHelperFunctions(unittest.TestCase):
    # 
    # Tests for markdown_to_blocks function
    # 
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
    
    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_markdown_to_blocks_no_newlines(self):
        md = "This is a single paragraph without newlines"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single paragraph without newlines"])
    
    def text_markdown_to_blocks_single_newlines(self):
        md = """
This is a paragraph that
has a single newline in one paragraph

And another paragraph
with another
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph that\nhas a single newline in one paragraph",
                "And another paragraph\nwith another",
            ],
        )
    
    def test_markdown_to_blocks_ending_double_newline(self):
        md = "This is a paragraph with an ending double newline\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a paragraph with an ending double newline"])
    
    def test_markdown_to_blocks_leading_double_newline(self):
        md = "\n\nThis is a paragraph with a leading double newline"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a paragraph with a leading double newline"])

    def test_markdown_to_blocks_leading_and_ending_double_newline(self):
        md = "\n\nThis is a paragraph with a leading and ending double newline\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a paragraph with a leading and ending double newline"])

    def test_markdown_to_blocks_triple_newline(self):
        md = "This is a paragraph with a triple newline\n\n\nIt's right there in the middle!"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph with a triple newline",
                "It's right there in the middle!",
            ],
        )

    # 
    # Tests for block_to_block_type function
    # 

    def test_block_to_block_type_paragraph(self):
        block = "This is a paragraph with some text."
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_heading(self):
        block = "# This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)
    
    def test_block_to_block_type_code_block(self):
        block = "```\nThis is a code block\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE_BLOCK)

    def test_block_to_block_type_blockquote(self):
        block = "> This is a blockquote\n> with multiple lines\n> of text"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.BLOCKQUOTE)
    
    def test_block_to_block_type_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_bad_ordered_list(self):
        block = "1. Item 1\n2. Item 2\n- Item 3"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    def test_block_to_block_type_bad_unordered_list(self):
        block = "- Item 1\n- Item 2\n1. Item 3"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    