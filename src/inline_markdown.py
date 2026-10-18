from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        delimited = node.text.split(delimiter)
        if len(delimited) % 2 != 1:
            raise Exception("odd number of delimiters found - perhaps a closing delimiter is missing")
        for i in range(0,len(delimited)):
            if i % 2 == 0:  #Evens
                if delimited[i] != "":
                    new_nodes.append(TextNode(delimited[i], TextType.TEXT))
            else:  #Odds
                new_nodes.append(TextNode(delimited[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    alt_text_urls = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return alt_text_urls

def extract_markdown_links(text):
    anchor_text_urls = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return anchor_text_urls

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if images == []:
            new_nodes.append(node)
            continue

        text_to_process = node.text
        for image in images:
            image_markdown = f"![{image[0]}]({image[1]})"
            sections = text_to_process.split(image_markdown, 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

            text_to_process = sections[1]
        if text_to_process != "":
            new_nodes.append(TextNode(text_to_process, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if links == []:
            new_nodes.append(node)
            continue

        text_to_process = node.text
        for link in links:
            link_markdown = f"[{link[0]}]({link[1]})"
            sections = text_to_process.split(link_markdown, 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

            text_to_process = sections[1]
        if text_to_process != "":
            new_nodes.append(TextNode(text_to_process, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    node_list = [TextNode(text,text_type=TextType.TEXT)]
    node_list = split_nodes_delimiter(node_list,delimiter="**",text_type=TextType.BOLD)
    node_list = split_nodes_delimiter(node_list,delimiter="_",text_type=TextType.ITALIC)
    node_list = split_nodes_delimiter(node_list,delimiter="`",text_type=TextType.CODE)
    node_list = split_nodes_image(node_list)
    node_list = split_nodes_link(node_list)
    return node_list


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    block_list = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:
            block_list.append(stripped_block)
    return block_list
