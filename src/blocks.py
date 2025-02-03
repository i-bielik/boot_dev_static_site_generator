import os


def markdown_to_blocks(text):
    blocks = text.split(os.linesep + os.linesep)
    filtered = filter(lambda x: x != "", blocks)
    return list(map(lambda x: x.strip(), filtered))
