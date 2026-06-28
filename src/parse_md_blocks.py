from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
import re
from textnode import text_node_to_html_node, TextNode, TextType
from parse_md_inline import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"
    LIST_ITEM = "list_item"


def markdown_to_blocks(markdown: str) -> list[str]: # take full md str return list of blocks
    blocks = markdown.split("\n\n")
    cleaned_blocks = []

    for block in blocks:
        stripped_block = block.strip()

        if stripped_block:
            cleaned_blocks.append(stripped_block)

    return cleaned_blocks
    

def block_to_block_type(block: str) -> BlockType: # take a single block str and return BlockType
    
    if "# " in block[:6] and block[0] == "#":
        return BlockType.HEADING
    
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    if block[0] == ">":
        if _line_check_helper(block, ">"): return BlockType.QUOTE
    
    if block[:2] == "- ":
        if _line_check_helper(block, "- "): return BlockType.UNORDERED
    
    if block[:3] == "1. ":
        if _line_check_helper(block, "N. "): return BlockType.ORDERED
    
    else:
        return BlockType.PARAGRAPH
    
def _line_check_helper(block: str, sym: str):
    lines = block.split("\n")
    for i, line in enumerate(lines, start=1):
        if "N" in sym:
            nsym = f"{i}. "
        else:
            nsym = sym

        if line[:len(nsym)] != nsym:
            return False
    return True


def markdown_to_html_node(markdown) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.QUOTE:
            quote_text = _strip_quote_markers(block)
            nodes.append(ParentNode("blockquote", _text_to_children(quote_text)))

        elif block_type == BlockType.UNORDERED:
            nodes.append(ParentNode("ul", _list_to_items(block, BlockType.UNORDERED)))

        elif block_type == BlockType.ORDERED:
            nodes.append(ParentNode("ol", _list_to_items(block, BlockType.ORDERED)))

        elif block_type == BlockType.LIST_ITEM:
            nodes.append(ParentNode("li", _text_to_children(block)))

        elif block_type == BlockType.CODE:
            code_text = block[4:-3]
            c_node = LeafNode("code", code_text)
            nodes.append(ParentNode("pre", [c_node]))

        elif block_type == BlockType.HEADING:
            hash_count = _count_hash(block)
            heading_text = block[hash_count + 1:]
            nodes.append(ParentNode(f"h{hash_count}", _text_to_children(heading_text)))

        elif block_type == BlockType.PARAGRAPH:
            space_div_block = block.replace("\n", " ")
            nodes.append(ParentNode("p", _text_to_children(space_div_block)))

        else:
            raise Exception("Block type doesn't exist.")
    
    parent = ParentNode("div", nodes)
    return parent


def _text_to_children(text) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes
    

def _list_to_items(block: str, block_type: BlockType) -> list[str]:
    list_item_nodes = []
    lines = block.split("\n")

    for i, line in enumerate(lines, start=1):
        if block_type == BlockType.UNORDERED:
            item_text = line[2:]

        elif block_type == BlockType.ORDERED:
            item_text = line[3:]

        else:
            raise ValueError("List item incorectly structured.")

        list_item_nodes.append(ParentNode("li", _text_to_children(item_text)))
    return list_item_nodes


def _count_hash(block: str) -> int:
    n = 0
    for char in block:
        if char == "#":
            n += 1
        else:
            break
    return n


def _strip_quote_markers(block: str) -> str:
    lines = block.split("\n")
    stripped_lines = []

    for line in lines:
        if line[:2] == "> ":
            stripped_lines.append(line[2:])
        else:
            stripped_lines.append(line[1:])

    return "\n".join(stripped_lines)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.strip("# ")
    raise Exception("No title block.")