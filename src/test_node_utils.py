import unittest

from node_utils import split_nodes_delimiter
from textnode import TextNode, TextType


class TestInlineSplitMarkdown(unittest.TestCase):
    def test_split_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_errors(self):
        node = TextNode("Invalid **markdown text.", TextType.NORMAL)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_not_type_normal(self):
        node = TextNode("Valid **markdown** text.", TextType.BOLD)
        expected = [node]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), expected)


if __name__ == "__main__":
    unittest.main()
