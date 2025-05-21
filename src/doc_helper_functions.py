from block_helper_functions import *
from inline_helper_functions import *
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType
import re

# Takes the string of a parent block and returns a List of child inline TextNodes
def text_to_children(text):
    text_nodes = text_to_textnodes(whitespace_stripper(text))
    html_nodes = list(map(text_node_to_html_node, text_nodes))
    return html_nodes

# Takes a block String and eliminates newlines while truncating horizontal whitespace
def whitespace_stripper(text):
    return re.sub(r"\s+", " ", text).strip()

# Clean the string within a code block of beginning and ending backticks
def code_block_cleaner(text):
    text = text.strip()
    if text.startswith("```\n") and text.endswith("```"):
        return text[4:-3]
    return text

# Strip markers from each line within a blockquote
def blockquote_cleaner(text):
    lines = text.split("\n")
    cleaned_lines = [line[2:] for line in lines if line.startswith("> ")]
    return "\n".join(cleaned_lines)

# Strip markers from each line within an unordered list
def unordered_list_cleaner(text):
    lines = text.split("\n")
    cleaned_lines = [line[2:] for line in lines if line.startswith("- ")]
    return cleaned_lines

# Strip markers from each line within an ordered list using regex
def ordered_list_cleaner(text):
    lines = text.split("\n")
    cleaned_lines = list(map(lambda line: re.sub(r"^\d+\.\s+", "", line), lines))
    return cleaned_lines

# Strip markers from beginning of a heading
def heading_cleaner(text):
    cleaned_line = text.lstrip("#").strip()
    return cleaned_line

# Determine level of heading based on number of '#' characters
def heading_level(text):
    level = 0
    while level < len(text) and text[level] == "#":
        level += 1
    return level

# Determines the type of block based on block_type and returns a new HTMLNode
# Includes children nodes based on text
def build_html_node(block_type, block_text):
    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode("p", text_to_children(block_text))
        case BlockType.HEADING:
            level = heading_level(block_text)
            return ParentNode(f"h{level}", text_to_children(heading_cleaner(block_text)))
        case BlockType.CODE_BLOCK:
            return ParentNode("pre", [text_node_to_html_node(TextNode(code_block_cleaner(block_text), TextType.CODE))])
        case BlockType.BLOCKQUOTE:
            return ParentNode("blockquote", text_to_children(blockquote_cleaner(block_text)))
        case BlockType.UNORDERED_LIST:
            list_items = unordered_list_cleaner(block_text)
            list_items = list(map(lambda item: ParentNode("li", text_to_children(item)), list_items))
            return ParentNode("ul", list_items)
        case BlockType.ORDERED_LIST:
            list_items = ordered_list_cleaner(block_text)
            list_items = list(map(lambda item: ParentNode("li", text_to_children(item)), list_items))
            return ParentNode("ol", list_items)
        case _:
            raise ValueError(f"Unknown block type: {block_type}")

# Takes a String of markdown and returns a div HTMLNode with all the blocks and their children
def markdown_to_html_node(markdown):
    new_nodes = []

    blocks = markdown_to_blocks(markdown) # Gets back a list of strings
    for block in blocks:
        block_type = block_to_block_type(block) # Gets back a BlockType
        new_node = build_html_node(block_type, block) # Gets back a ParentNode with children
        new_nodes.append(new_node)
    
    return ParentNode("div", new_nodes)
        