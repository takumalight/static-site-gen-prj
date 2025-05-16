import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("div", "Hello world", None, {"border":"1px solid black", "color":"#fff"})
        self.assertEqual(node.props_to_html(), ' border="1px solid black" color="#fff"')
    
    def test_props_2(self):
        node = HTMLNode("a", "Check this link!", None, {"href":"http://example.com", "target":"_blank"})
        self.assertEqual(node.props_to_html(), ' href="http://example.com" target="_blank"')
    
    def test_props_3(self):
        node = HTMLNode("div", None, [HTMLNode("p", "Hello world", None, {"class":"text"})], {"style":"color: red;"})
        self.assertEqual(node.props_to_html(), ' style="color: red;"')
    
    def test_no_props(self):
        node = HTMLNode("div", "Hello world")
        self.assertEqual(node.props_to_html(), "")

if __name__ == "__main__":
    unittest.main()