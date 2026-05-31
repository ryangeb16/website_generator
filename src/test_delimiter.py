import unittest

from textnode import TextNode, TextType
from node_delimiter import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        # 1. Arrange: set up your input
        node = TextNode("hello `world` bye", TextType.TEXT)
        # 2. Act: call the function
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        # 3. Assert: compare against what you expect
        self.assertEqual(new_nodes, [
            # the TextNodes you expect back
            TextNode("hello ", TextType.TEXT),
            TextNode("world", TextType.CODE),
            TextNode(" bye", TextType.TEXT)
        ])

    def test_bold_first(self):
        # 1. Arrange: set up your input
        node = TextNode("**This** is my house", TextType.TEXT)
        # 2. Act: call the function
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        # 3. Assert: compare against what you expect
        self.assertEqual(new_nodes, [
            # the TextNodes you expect back
            TextNode("This", TextType.BOLD),
            TextNode(" is my house", TextType.TEXT)
        ])

    def test_italic_multiple(self):
        # 1. Arrange: set up your input
        node = TextNode("This __sentence__ has multiple __italics__", TextType.TEXT)
        # 2. Act: call the function
        new_nodes = split_nodes_delimiter([node], "__", TextType.ITALIC)
        # 3. Assert: compare against what you expect
        self.assertEqual(new_nodes, [
            # the TextNodes you expect back
            TextNode("This ", TextType.TEXT),
            TextNode("sentence", TextType.ITALIC),
            TextNode(" has multiple ", TextType.TEXT),
            TextNode("italics", TextType.ITALIC)
        ])


if __name__ == "__main__":
    unittest.main()