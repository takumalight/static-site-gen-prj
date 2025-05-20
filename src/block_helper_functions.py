from blocknode import BlockType
from htmlnode import *

# Takes a String of markdown and returns a List of block Strings
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = map(lambda block: block.strip(), blocks)
    blocks = list(filter(lambda block: block != "", blocks))
    return blocks

# Takes a block String and returns a BlockType
def block_to_block_type(block):
    match block:
        case block if block.startswith("# "):
            return BlockType.HEADING
        case block if block.startswith("```") and block.endswith("```"):
            return BlockType.CODE_BLOCK
        case block if all(map(lambda line: line.startswith("> "), block.split("\n"))):
            return BlockType.BLOCKQUOTE
        case block if all(map(lambda line: line.startswith("- "), block.split("\n"))):
            return BlockType.UNORDERED_LIST
        case block if all(map(lambda line: line[0].isdigit() and line[1:3] == ". ", block.split("\n"))):
            return BlockType.ORDERED_LIST
        case _:
            return BlockType.PARAGRAPH
