import os
from pathlib import Path
import re

from htmlnode import ParentNode
from node_utils import text_to_textnodes
from textnode import text_node_to_html_node


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    source_dir = Path(dir_path_content)
    md_files = source_dir.glob("**/*.md")

    for md in md_files:
        parts = list(md.parts)
        p_from = str(md)
        parts[0] = dest_dir_path
        to_path = "/".join(parts).replace(".md", ".html")
        generate_page(p_from, template_path, to_path)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as md_file:
        md = md_file.read()

    title = extract_title(md)
    md_to_html = markdown_to_html_node(md).to_html()

    with open(template_path, "r") as tmplt:
        html_template = tmplt.read()

    new_html = html_template.format(Title=title, Content=md_to_html)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as dest_file:
        dest_file.write(new_html)


def extract_title(text):
    for line in text.split(os.linesep):
        if re.search(r"^#{1} \S", line):
            return line.replace("# ", "").strip()

    raise Exception("No heading 1 provided in given text")


def markdown_to_blocks(text):
    blocks = text.split(os.linesep + os.linesep)
    filtered = filter(lambda x: x != "", blocks)
    return list(map(lambda x: x.strip(), filtered))


def md_block_to_block_type(block: str) -> str:
    lines = block.split(os.linesep)

    # Check for heading
    if re.match(r"^#{1,6} \S", lines[0]):
        return "heading"

    # Check for code block
    if block.startswith("```") and block.endswith("```"):
        return "code"

    # Check for quote block
    if all(line.startswith(">") for line in lines):
        return "quote"

    # Check for unordered list
    if all(re.match(r"^[-*] \S", line) for line in lines):
        return "unordered_list"

    # Check for ordered list
    ordered_list_pattern = r"^(\d+)\. \S"
    numbers = [
        int(re.match(ordered_list_pattern, line).group(1))
        for line in lines
        if re.match(ordered_list_pattern, line)
    ]
    if numbers and numbers == list(range(1, len(numbers) + 1)):
        return "ordered_list"

    # Default to paragraph
    return "paragraph"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = md_block_to_block_type(block)
    if block_type == "paragraph":
        return paragraph_to_html_node(block)
    if block_type == "heading":
        return heading_to_html_node(block)
    if block_type == "code":
        return code_to_html_node(block)
    if block_type == "ordered_list":
        return olist_to_html_node(block)
    if block_type == "unordered_list":
        return ulist_to_html_node(block)
    if block_type == "quote":
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    nodes = text_to_textnodes(text)
    children = [text_node_to_html_node(node) for node in nodes]
    return children


def paragraph_to_html_node(block):
    paragraph = " ".join(block.split("\n"))
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    heading_sign = block.split(" ")[0]
    level = heading_sign.count("#")
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block.replace("#", "").lstrip()
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
