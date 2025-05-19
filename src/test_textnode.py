import unittest
from textnode import *
from htmlnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("Link Goes Here", TextType.LINK, "http://example.com")
        self.assertNotEqual(node, node2)

    def test_url_no_link(self):
        node = TextNode("Link Goes Here", TextType.LINK)
        node2 = TextNode("Link Goes Here", TextType.LINK, "http://example.com")
        self.assertNotEqual(node, node2)

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "http://example.com/image.png")
        self.assertEqual(node.url, "http://example.com/image.png")
        self.assertEqual(node.__repr__(), "TextNode(This is an image, image, http://example.com/image.png)")
    
    def test_diff_test(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_missing_type(self):
        node = TextNode("This is a text node", None)
        node2 = TextNode("This is a text node", "")
        self.assertNotEqual(node, node2)
    
    def test_missing_text(self):
        node = TextNode("", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_image_textnode(self):
        node = TextNode("This is an image", TextType.IMAGE, "http://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "http://example.com/image.png", "alt": "This is an image"})
        self.assertEqual(html_node.value, "")

    def test_bold_textnode(self):
        node = TextNode("This is a bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text")
        self.assertEqual(html_node.props, None)


if __name__ == "__main__":
    unittest.main()
