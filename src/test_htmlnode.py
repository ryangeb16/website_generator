import unittest
from htmlnode import HTMLNode, LeafNode,ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_noprop(self):
        node = HTMLNode()
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_oneprop(self):
        node = HTMLNode(props={"href": "https://www.example.com"})
        result = node.props_to_html()
        self.assertEqual(result,' href="https://www.example.com"')

    def test_multprop(self):
        node = HTMLNode(props={"href": "https://www.example.com", "target": "_blank"})
        result = node.props_to_html()
        self.assertEqual(result,' href="https://www.example.com" target="_blank"')

class TestHTMLLeaf(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_leaf_to_html_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

class TestHTMLParent(unittest.TestCase):
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

