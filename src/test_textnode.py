import unittest

from textnode import (
    TextNode,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):

        normal_node = TextNode("First test node", "bold", "first random link")
        normal_node_2 = TextNode("First test node", "bold", "first random link")
        self.assertEqual(normal_node, normal_node_2)

        node_without_url = TextNode("Second test node", "bold")
        node_without_url_2 = TextNode("Second test node", "bold")
        self.assertEqual(node_without_url, node_without_url_2)

    def test_not_eq(self):

        node_with_different_text_type = TextNode("Third test node", "italic")
        node_with_different_text_type_2 = TextNode("Third test node", "bold")
        self.assertNotEqual(
            node_with_different_text_type, node_with_different_text_type_2
        )

        node_with_different_text = TextNode("Fourth test node", "bold")
        node_with_different_text_2 = TextNode("Fifth test node", "bold")
        self.assertNotEqual(node_with_different_text, node_with_different_text_2)

    def test_split_nodes_delimiter(self):
        code_node = TextNode("This is text with a `code block` word", "text")
        invalid_bold_node = TextNode("This is the text with *bold* word", "bold")

        bold_node = TextNode("This is the **bold text**", "text")

        double_bold_node = TextNode(
            "This is the **first bold** with the **second bold**", "text"
        )

        italic_node = TextNode("This is text with a *italic hehe* word", "text")

        self.assertEqual(
            split_nodes_delimiter(
                [italic_node, invalid_bold_node], "*", "italic"
            ).__repr__(),
            "[TextNode(This is text with a , text, None), TextNode(italic hehe, italic, None), TextNode( word, text, None), TextNode(This is the text with *bold* word, bold, None)]",
        )

        self.assertEqual(
            split_nodes_delimiter([code_node], "`", "code").__repr__(),
            "[TextNode(This is text with a , text, None), TextNode(code block, code, None), TextNode( word, text, None)]",
        )

        self.assertEqual(
            split_nodes_delimiter([bold_node], "**", "bold").__repr__(),
            "[TextNode(This is the , text, None), TextNode(bold text, bold, None)]",
        )

        # print(split_nodes_delimiter([double_bold_node, code_node, italic_node],"**","bold"))

    def test_delim_bold_double(self):
        node = TextNode("This is text with a **bolded** word and **another**", "text")
        new_nodes = split_nodes_delimiter([node], "**", "bold")
        self.assertListEqual(
            [
                TextNode("This is text with a ", "text"),
                TextNode("bolded", "bold"),
                TextNode(" word and ", "text"),
                TextNode("another", "bold"),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", "text")
        new_nodes = split_nodes_delimiter([node], "**", "bold")
        new_nodes = split_nodes_delimiter(new_nodes, "*", "italic")
        self.assertListEqual(
            [
                TextNode("bold", "bold"),
                TextNode(" and ", "text"),
                TextNode("italic", "italic"),
            ],
            new_nodes,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imageur.com/zjjcJKZ.png)",
            "text",
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", "text"),
                TextNode("image", "image", "https://i.imageur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            "text",
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", "image", "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imageur.com/zjjcJKZ.png) and another ![second image](https://i.imageur.com/3elNhQu.png)",
            "text",
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", "text"),
                TextNode("image", "image", "https://i.imageur.com/zjjcJKZ.png"),
                TextNode(" and another ", "text"),
                TextNode("second image", "image", "https://i.imageur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            "text",
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", "text"),
                TextNode("link", "link", "https://boot.dev"),
                TextNode(" and ", "text"),
                TextNode("another link", "link", "https://blog.boot.dev"),
                TextNode(" with text that follows", "text"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imageur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", "text"),
                TextNode("text", "bold"),
                TextNode(" with an ", "text"),
                TextNode("italic", "italic"),
                TextNode(" word and a ", "text"),
                TextNode("code block", "code"),
                TextNode(" and an ", "text"),
                TextNode("image", "image", "https://i.imageur.com/zjjcJKZ.png"),
                TextNode(" and a ", "text"),
                TextNode("link", "link", "https://boot.dev"),
            ],
            nodes,
        )


if __name__ == "__main__":
    unittest.main()
