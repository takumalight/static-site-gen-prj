import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
