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

    # Tests for split_nodes_delimiter function

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

    # Tests for extract_markdown_images function
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with a ![image1](https://i.imgur.com/zjjcJKZ.png) and ![image2](https://i.imgur.com/asdwqwe.png)"
        )
        self.assertListEqual(
            [
                ("image1", "https://i.imgur.com/zjjcJKZ.png"),
                ("image2", "https://i.imgur.com/asdwqwe.png"),
            ],
            matches
        )
    
    def test_extract_markdown_images_link_no_image(self):
        matches = extract_markdown_images(
            "This is text with a [link](https://example.com) and no image"
        )
        self.assertListEqual([], matches)

    def test_extract_image_no_image(self):
        matches = extract_markdown_images(
            "This is text with no image"
        )
        self.assertListEqual([], matches)

    # Tests for extract_markdown_links function
    
    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This is text with a [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches
        )
    
    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links(
            "This is text with a [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)
    
    def test_extract_markdown_links_image_no_link(self):
        matches = extract_markdown_links("this is text with an ![image](https://i.imgur.com/example.png) and no link")
        self.assertListEqual([], matches)
    
    def test_extract_link_no_link(self):
        matches = extract_markdown_links(
            "This is text with no link"
        )
        self.assertListEqual([], matches)

    # Tests for split_nodes_image function
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_starting_image(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png) at the beginning", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" at the beginning", TextType.TEXT),
            ],
            new_nodes
        )
    
    def test_split_images_ending_image(self):
        node = TextNode("Text ends with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text ends with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes
        )

    def test_split_images_link_no_image(self):
        node = TextNode("Text with a [link](https://example.com) and no image", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("Text with a [link](https://example.com) and no image", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_images_with_link(self):
        node = TextNode("Text with ![image](https://i.imgur.com/zjjcJKZ.png) and [link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and [link](https://example.com)", TextType.TEXT)
            ],
            new_nodes
        )

    # Tests for split_nodes_link function
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [to boot dev](https://www.boot.dev) and another [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )
    
    def test_split_links_starting_link(self):
        node = TextNode("[Starting link](https://www.boot.dev) at the beginning", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Starting link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" at the beginning", TextType.TEXT),
            ],
            new_nodes
        )

    def test_split_links_ending_link(self):
        node = TextNode("Text end with a [link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text end with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes
        )
    
    def test_split_links_with_image(self):
        node = TextNode("Text with ![image](https://imgur.com/example.png) and [link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text with ![image](https://imgur.com/example.png) and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com")
            ],
            new_nodes
        )
    
    def test_leading_link_with_image(self):
        node = TextNode("[A link](https://example.com) that leads a string with a ![really cool image alt](https://imgur.com/example.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("A link", TextType.LINK, "https://example.com"),
                TextNode(" that leads a string with a ![really cool image alt](https://imgur.com/example.png)", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_links_image_no_link(self):
        node = TextNode("Text with an ![image](https://i.imgur.com/example.png) and no link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("Text with an ![image](https://i.imgur.com/example.png) and no link", TextType.TEXT)
            ],
            new_nodes
        )