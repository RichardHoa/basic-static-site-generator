import unittest

from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode,
    text_node_to_html_node,
    markdown_to_html_node,
    extract_title,
)
from textnode import TextNode


class TestHTMLNode(unittest.TestCase):

    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(tag=p, value=What a strange world, children=None, props={'class': 'primary'})",
        )

    def test_leaf_node_full_parameters(self):
        leaf_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            leaf_node.to_html(), '<a  href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_node_no_tag(self):
        leaf_node = LeafNode(None, "Click me!")
        self.assertEqual(leaf_node.to_html(), "Click me!")

    def test_leaf_node_no_value(self):
        with self.assertRaises(Exception) as Context:
            LeafNode("a", None).to_html()
        self.assertTrue("Value cannot be None" in str(Context.exception))

    def test_parent_node_full(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        # print(node.to_html())
        self.assertEqual(
            node.to_html(),
            "<p><b >Bold text</b>Normal text<i >italic text</i>Normal text</p>",
        )

    def test_parent_node_none_tag(self):
        node = ParentNode(
            None,
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        with self.assertRaises(Exception) as Context:
            node.to_html()
        self.assertTrue("Tag cannot be None" in str(Context.exception))

    def test_parent_node_none_children(self):
        node = ParentNode(
            "p",
            None,
        )
        with self.assertRaises(Exception) as Context:
            node.to_html()
        self.assertTrue("Children cannot be None" in str(Context.exception))

    def test_text_node_to_html_node(self):
        text_node = TextNode("First test node", "text")

        bold_node = TextNode("First test node", "bold")

        italic_node = TextNode("First test node", "italic")

        code_node = TextNode("First test node", "code")

        a_node = TextNode("First test node", "link", "https/stupidlink/online")

        img_node = TextNode("First test node", "image", "https/stupidlink/online")
        self.assertEqual(text_node_to_html_node(text_node).to_html(), "First test node")
        self.assertEqual(
            text_node_to_html_node(bold_node).to_html(), "<b >First test node</b>"
        )
        self.assertEqual(
            text_node_to_html_node(italic_node).to_html(), "<i >First test node</i>"
        )
        self.assertEqual(
            text_node_to_html_node(code_node).to_html(), "<code >First test node</code>"
        )
        self.assertEqual(
            text_node_to_html_node(a_node).to_html(),
            '<a  href="https/stupidlink/online">First test node</a>',
        )
        self.assertEqual(
            text_node_to_html_node(img_node).to_html(),
            '<img  src="https/stupidlink/online" alt="First test node"/>',
        )

    def test_complicated_paragraph(self):
        md = """
This is a paragraph with **bold** text with *italics* text with `code` text

### This is a h3 heading

This is a standard paragraph

This is a paragraph with **bold** text

This is a paragraph with *italics* text

This is a paragraph with `code` text


This is some image ![image](https://i.imageur.com/zjjcJKZ.png) ![second image](https://i.imageur.com/3elNhQu.png)

This is some link [boot.dev](https://boot.dev) [youtube](https://youtube.com)


``` 
This is some javascript code
```

* Unordered list syntax 1

- Underordered list syntax 2

1. Ordered list number
2. Ordered list number

####### This is an invalid heading, which is being treated as a paragraph
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            """<div><p>This is a paragraph with <b >bold</b> text with <i >italics</i> text with <code >code</code> text</p><h3 > This is a h3 heading</h3><p>This is a standard paragraph</p><p>This is a paragraph with <b >bold</b> text</p><p>This is a paragraph with <i >italics</i> text</p><p>This is a paragraph with <code >code</code> text</p><p>This is some image <img  src="https://i.imageur.com/zjjcJKZ.png" alt="image"/> <img  src="https://i.imageur.com/3elNhQu.png" alt="second image"/></p><p>This is some link <a  href="https://boot.dev">boot.dev</a> <a  href="https://youtube.com">youtube</a></p><pre><code >``` 
This is some javascript code</code></pre><ul><li>Unordered list syntax 1</li></ul><ul><li>Underordered list syntax 2</li></ul><ol><li>Ordered list number</li><li>Ordered list number</li></ol><p>####### This is an invalid heading, which is being treated as a paragraph</p></div>""",
        )

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            """<div><p>This is <b >bolded</b> paragraph
text in a p
tag here</p></div>""",
        )


if __name__ == "__main__":
    unittest.main()
