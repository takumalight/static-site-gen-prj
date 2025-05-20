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
    matches = re.findall(r"!\[([^]]+)\]\(([^)]+)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^]]+)\]\(([^)]+)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.TEXT:
            image_tuples = extract_markdown_images(node.text)
            working_string = node.text
            for image_alt, image_src in image_tuples:
                parts = working_string.split(f"![{image_alt}]({image_src})", 1)
                if(parts[0] != ""):
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_src))
                if len(parts) > 1:
                    working_string = parts[1]
            if working_string != "":
                new_nodes.append(TextNode(working_string, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.TEXT:
            link_tuples = extract_markdown_links(node.text)
            working_string = node.text
            for link_text, link_url in link_tuples:
                parts = working_string.split(f"[{link_text}]({link_url})", 1)
                if(parts[0] != ""):
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
                if len(parts) > 1:
                    working_string = parts[1]
            if working_string != "":
                new_nodes.append(TextNode(working_string, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    new_textnode = TextNode(text, TextType.TEXT)
    new_nodes = []
    new_nodes = split_nodes_image([new_textnode])
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    return new_nodes