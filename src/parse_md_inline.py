from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        # Process only the nodes whoose type is TEXT.
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        
        if len(parts) == 1:
            new_nodes.append(node)
            continue

        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid syntax, unmatched delimiter '{delimiter}'")
        
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]: # return alt text and URL
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def _split_nodes_by_markdown(old_nodes, extractor, text_type, markdown_builder):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extractor(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        remaining_text = node.text

        for label, url in matches:
            markdown = markdown_builder(label, url)
            sections = remaining_text.split(markdown, 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(label, text_type, url))
            remaining_text = sections[1]

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes):
    return _split_nodes_by_markdown(
        old_nodes,
        extract_markdown_images,
        TextType.IMAGE,
        lambda alt, url: f"![{alt}]({url})",
    )

def split_nodes_link(old_nodes):
    return _split_nodes_by_markdown(
        old_nodes,
        extract_markdown_links,
        TextType.LINK,
        lambda text, url: f"[{text}]({url})",
    )


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

