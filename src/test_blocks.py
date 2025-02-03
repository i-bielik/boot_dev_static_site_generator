import unittest

from src.blocks import markdown_to_blocks, md_block_to_block_type


class TestHTMLNode(unittest.TestCase):
    def test_text_to_blocks(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(md_block_to_block_type("# Heading"), "heading")
        self.assertEqual(md_block_to_block_type("###### Small Heading"), "heading")

    def test_code_block(self):
        self.assertEqual(md_block_to_block_type("```\ncode\n```"), "code")

    def test_quote_block(self):
        self.assertEqual(md_block_to_block_type("> Quote\n> Another line"), "quote")

    def test_unordered_list(self):
        self.assertEqual(md_block_to_block_type("- Item 1\n- Item 2"), "unordered_list")
        self.assertEqual(md_block_to_block_type("* Item 1\n* Item 2"), "unordered_list")

    def test_ordered_list(self):
        self.assertEqual(md_block_to_block_type("1. First\n2. Second\n3. Third"), "ordered_list")

    def test_paragraph(self):
        self.assertEqual(md_block_to_block_type("This is a normal paragraph."), "paragraph")

    def test_mixed_content(self):
        self.assertEqual(md_block_to_block_type("1. First\n3. Incorrect"), "paragraph")
        self.assertEqual(md_block_to_block_type("> Quote\nNormal text"), "paragraph")


if __name__ == "__main__":
    unittest.main()
