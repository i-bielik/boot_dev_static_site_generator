import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter: str, text_type):
    """
    Example:

    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    It should return
    [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
    ]
    """
    result = []

    for item in old_nodes:
        if item.text_type != TextType.NORMAL:
            result.append(item)
            continue
        if item.text.count(delimiter) != 2:
            raise ValueError("Invalid Markdown format")
        for i, v in enumerate(item.text.split(delimiter)):
            if i == 1:
                result.append(TextNode(v, text_type))
            else:
                result.append(TextNode(v, TextType.NORMAL))

    return result


def extract_markdown_images(text):
    match_alt = re.findall(r"!\[(.*?)\]", text)
    match_url = re.findall(r"\]\((.*?)\)", text)

    return list(zip(match_alt, match_url))


def extract_markdown_links(text):
    match_alt = re.findall(r"\[(.*?)\]", text)
    match_url = re.findall(r"\]\((.*?)\)", text)

    return list(zip(match_alt, match_url))
