from block import markdown_to_blocks, block_to_block_type

from textnode import text_to_textnodes
import re


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        pass

    def props_to_html(self):
        html = ""
        if self.props is not None:
            for key, value in self.props.items():
                html += f' {key}="{value}"'
            return html
        return html

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Value cannot be None")
        elif self.tag is None:
            return f"{self.value}"
        else:
            if self.tag == "img":
                return f"<{self.tag} {self.props_to_html()}/>"
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag cannot be None")
        if self.children is None:
            raise ValueError("Children cannot be None")
        else:
            start_string = f"<{self.tag}>"
            content = ""
            end_string = f"</{self.tag}>"

        for child in self.children:
            content += child.to_html()

        return start_string + content + end_string

    def __repr__(self):
        return (
            f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"
        )


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case "text":
            return LeafNode(None, text_node.text)
        case "bold":
            return LeafNode("b", text_node.text)
        case "italic":
            return LeafNode("i", text_node.text)
        case "code":
            return LeafNode("code", text_node.text)
        case "link":
            ref_dict = {"href": text_node.url}
            return LeafNode("a", text_node.text, ref_dict)
        case "image":
            ref_dict = {"src": text_node.url, "alt": text_node.text}
            return LeafNode("img", "", ref_dict)
        case _:
            raise Exception("Invalid Text Type")


def markdown_to_html_node(markdown):
# Currently this function return a rather weird stupid html format
    props_list = []
    # Get markdown document into blocks
    blocks = markdown_to_blocks(markdown)


    for block in blocks:
        # Get all the words
        words = block.split()
        # Get the block type
        block_type = block_to_block_type(block)

        # If the block is a list, process it to remove ordered and unordered lists syntax
        if block_type == "unordered_list" or block_type == "ordered_list":
            list_children_nodes = helper_markdown_to_html_list(block)
        
        match block_type:
            case "heading":
                # Count the # to the heading numer. One # is h1,  ## is h2, etc
                heading_number = words[0].count("#")
                # If heading number is 6, it's invalid and the block is considered as a paragraph
                if heading_number > 6:
                   helper_markdown_to_html_paragraph(block, props_list) 
                else:
                    # Remove the # headings out of the block, remain other # if any
                    formatted_block = re.sub(r"#+", "", block, 1)
                    props_list.append(
                        LeafNode(tag=f"h{heading_number}", value=formatted_block)
                    )
            case "quote":
                formatted_block = block.removeprefix("> ").removesuffix("\n")
                props_list.append(LeafNode(tag="blockquote", value=formatted_block))
            case "unordered_list":
                props_list.append(ParentNode(tag="ul", children=list_children_nodes))
            case "ordered_list":
                props_list.append(ParentNode(tag="ol", children=list_children_nodes))
            case "code":
                # Remove all the code syntax, syntax: <pre><code></code></pre>
                code_value = block.removeprefix("```\n").removesuffix("\n```")
                code_html = LeafNode(tag="code", value=code_value)
                props_list.append(ParentNode(tag="pre", children=[code_html]))
            case "paragraph":
                helper_markdown_to_html_paragraph(block, props_list)

    return ParentNode(tag="div", children=props_list)

def helper_markdown_to_html_paragraph(block, props_list):
    children_leaf_node_list = []
    text_nodes = text_to_textnodes(block)
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children_leaf_node_list.append(html_node)
    props_list.append(ParentNode(tag="p", children=children_leaf_node_list))

def helper_markdown_to_html_list(block):
    # Get all the lines
    lines = block.split("\n")
    list_children_nodes = []

    # Helper counter to remove all the ordered list syntax
    counter_ordererd_list = 1
    for line in lines:
        li_children_list = []
        # Get rid of all the list syntax
        formatted_line = (
            line.removeprefix(f"{counter_ordererd_list}. ")
            .removeprefix("* ")
            .removeprefix("- ")
        )
        # Convert the formatted line to text nodes
        text_nodes = text_to_textnodes(formatted_line)
        for text_node in text_nodes:
            # For every text node, add it html node version to the children list of the parent li node
            singular_html_node = text_node_to_html_node(text_node)
            li_children_list.append(singular_html_node)

        list_children_nodes.append(ParentNode(tag="li", children=li_children_list))
        counter_ordererd_list += 1 
    return list_children_nodes

def extract_title(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    
    
    block_type = block_to_block_type(markdown_blocks[0])
    # print(block_type)
    if block_type == "heading":
        # print(blocks[0])
        return markdown_blocks[0].removeprefix("# ").strip()
    else:
        raise Exception("A post must have an h1 header")