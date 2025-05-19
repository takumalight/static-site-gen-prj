import unittest
from helper_functions import *
from textnode import *
from htmlnode import *

class TestSplitDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is a string with a `code block` in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is a string with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_unclosed(self):
        node = TextNode("This is a **bold text string with an unclosed delimiter", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)
    
    def test_split_nodes_delimiter_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [TextNode("", TextType.TEXT)]
        self.assertEqual(new_nodes, expected_nodes)
    
    def test_split_nodes_delimiter_italics_text_type(self):
        node = TextNode("This whole string is italicized", TextType.ITALIC)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("This whole string is italicized", TextType.ITALIC)
        ]
        self.assertEqual(new_nodes, expected_nodes)
    
    def test_split_nodes_delimiter_empty_nodes(self):
        new_nodes = split_nodes_delimiter([], "**", TextType.BOLD)
        expected_nodes = []
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_multiple_nodes(self):
        node1 = TextNode("This string has a `code block` in it", TextType.TEXT)
        node2 = TextNode("This string has a **bold text** in it", TextType.TEXT)
        node3 = TextNode("Another string with a `code block` in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2, node3], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This string has a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" in it", TextType.TEXT),
            TextNode("This string has a **bold text** in it", TextType.TEXT),
            TextNode("Another string with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)
    
    def test_successive_splits(self):
        node = TextNode("This is a string with a `code block` and **bold text** in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is a string with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)
    
    def test_leading_delimiter(self):
        node = TextNode("**bold text** at the beginning", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" at the beginning", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_trailing_delimiter(self):
        node = TextNode("Text that ends _italicized_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("Text that ends ", TextType.TEXT),
            TextNode("italicized", TextType.ITALIC),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)