from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode

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