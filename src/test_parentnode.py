import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_parent_with_no_tag(self):
        node = ParentNode(None, [ParentNode("p", "Hello, world!")], {"border": "1px solid black"})
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_parent_with_no_children(self):
        node = ParentNode("div", None, {"style": "color: red"})
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_fibbonaci_family(self):
        gc_node_1_1 = LeafNode("b", "grandchild 1.1")
        gc_node_1_2 = LeafNode("b", "grandchild 1.2")
        gc_node_1_3 = LeafNode("b", "grandchild 1.3")
        gc_node_2_1 = LeafNode("b", "grandchild 2.1")
        gc_node_2_2 = LeafNode("b", "grandchild 2.2")
        gc_node_2_3 = LeafNode("b", "grandchild 2.3")
        c_node_1 = ParentNode("span", [gc_node_1_1, gc_node_1_2, gc_node_1_3])
        c_node_2 = ParentNode("span", [gc_node_2_1, gc_node_2_2, gc_node_2_3])
        p_node = ParentNode("div", [c_node_1, c_node_2], {"border": "1px solid black"})
        self.assertEqual(p_node.to_html(), "<div border=\"1px solid black\"><span><b>grandchild 1.1</b><b>grandchild 1.2</b><b>grandchild 1.3</b></span><span><b>grandchild 2.1</b><b>grandchild 2.2</b><b>grandchild 2.3</b></span></div>")

    def test_nested_parent_with_no_childern(self):
        node = ParentNode("div", [ParentNode("p", None)], {"style": "color: red"})
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_two_children_one_grandchild(self):
        gc_node = LeafNode("b", "grandchild")
        c_node_1 = ParentNode("span", [gc_node])
        c_node_2 = LeafNode("p", "child")
        p_node = ParentNode("div", [c_node_1, c_node_2], {"border": "1px solid black"})
        self.assertEqual(p_node.to_html(), "<div border=\"1px solid black\"><span><b>grandchild</b></span><p>child</p></div>")



if __name__ == "__main__":
    unittest.main()