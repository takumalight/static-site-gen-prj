from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.TEXT:
            string_parts = node.text.split(delimiter)
            if len(string_parts) % 2 == 0:
                raise Exception("Closing delimiter is missing")
            for i, part in enumerate(string_parts):
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"\[([^]]+)\]\(([^)]+)\)", text)
    return [(match[0], match[1]) for match in matches]

# text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
# print(extract_markdown_links(text))
# [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
def extract_markdown_links(text):
    matches = re.findall(r"\[([^]]+)\]\(([^)]+)\)", text)
    return [(match[0], match[1]) for match in matches]