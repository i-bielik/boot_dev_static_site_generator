import re
import os
from textnode import TextNode, TextType


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


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
        sections = item.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i, val in enumerate(sections):
            if val == "":
                continue
            if i % 2 == 1:
                result.append(TextNode(val, text_type))
            else:
                result.append(TextNode(val, TextType.NORMAL))

    return result


def split_nodes_link(old_nodes):
    results = []

    for item in old_nodes:
        link_data = extract_markdown_links(item.text)
        if item.text_type != TextType.NORMAL or link_data == []:
            results.append(item)
            continue
        start_text = item.text
        for link in link_data:
            sections = start_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                results.append(TextNode(sections[0], TextType.NORMAL))
            results.append(TextNode(link[0], TextType.LINK, link[1]))
            start_text = sections[1]
        if start_text != "":
            results.append(TextNode(start_text, TextType.NORMAL))

    return results


def split_nodes_image(old_nodes):
    results = []

    for item in old_nodes:
        image_data = extract_markdown_images(item.text)
        if item.text_type != TextType.NORMAL or image_data == []:
            results.append(item)
            continue
        start_text = item.text
        for image in image_data:
            sections = start_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                results.append(TextNode(sections[0], TextType.NORMAL))
            results.append(TextNode(image[0], TextType.IMAGE, image[1]))
            start_text = sections[1]
        if start_text != "":
            results.append(TextNode(start_text, TextType.NORMAL))

    return results


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches
