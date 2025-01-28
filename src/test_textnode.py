import unittest

from src.htmlnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text_to_html_conversion(self):
        node = TextNode("This is a text node", None)
        node2 = TextNode("This is a text node", TextType.NORMAL)
        with self.assertRaises(Exception):
            text_node_to_html_node(node)
        self.assertEqual(
            text_node_to_html_node(node2).to_html(), LeafNode(None, node2.text, {}).to_html()
        )


if __name__ == "__main__":
    unittest.main()
