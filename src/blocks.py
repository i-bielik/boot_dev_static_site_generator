import os
import re


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
