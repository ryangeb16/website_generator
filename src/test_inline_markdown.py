import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks


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
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_2images(self):
        matches = extract_markdown_images(
            "This is text with one ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://www.boot.dev/img/bootdev-logo-full-150.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"),("image","https://www.boot.dev/img/bootdev-logo-full-150.png")], matches)

    def test_extract_markdown_0images(self):
        matches = extract_markdown_images(
            "This is text without an image"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links_on_image(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and an ![image](https://www.boot.dev/img/bootdev-logo-full-150.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

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
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        input_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        node_list = text_to_textnodes(input_text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            node_list
        )


if __name__ == "__main__":
    unittest.main()