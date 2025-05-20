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
    

# Determines the type of block based on block_type and returns a new HTMLNode
# Includes children nodes based on text
def build_html_node(block_type, block_text):
    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode("p", text_to_children(block_text))
        case BlockType.HEADING:
            level = block.count("#")
            return ParentNode(f"h{level}", text_to_children(block))
        case BlockType.CODE_BLOCK:
            return ParentNode("pre", [LeafNode("code", block_text)])
        case BlockType.BLOCKQUOTE:
            return ParentNode("blockquote", text_to_children(block_text))
        case BlockType.UNORDERED_LIST:
            return ParentNode("ul", text_to_children(block_text))
        case BlockType.ORDERED_LIST:
            return ParentNode("ol", text_to_children(block_text))
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
        