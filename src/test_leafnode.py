import unittest
from htmlnode import *

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_with_one_prop(self):
        node = LeafNode("a", "Click here", {"href": "http://example.com"})
        self.assertEqual(node.to_html(), '<a href="http://example.com">Click here</a>')

    def test_leaf_with_two_props(self):
        node = LeafNode("span", "hello", {"id": "weirdospan", "style": "color: #006"})
        self.assertEqual(node.to_html(), '<span id="weirdospan" style="color: #006">hello</span>')

    # This project assumes no leaf node will ever be an image/self-closing tag
    def test_value_error_with_img(self):
        node = LeafNode("img", None, {"src": "image.png"})
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()