from extract_link import extract_markdown_links, extract_markdown_images



class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        else:
            return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result_nodes = []

    for node in old_nodes:
        if node.text_type == "text":
            text_list = node.text.split(delimiter)
            if len(text_list) % 2 == 0:
                raise Exception(
                    "One of the markdown line has incorrect inline format (bold,italic, quote), please check again"
                )
            for i in range(len(text_list)):
                if text_list[i] == "":
                    continue
                if i % 2 == 0:
                    result_nodes.append(TextNode(text_list[i], "text"))
                else:
                    result_nodes.append(TextNode(text_list[i], text_type))
        else:
            result_nodes.append(node)
    return result_nodes


def split_nodes_image(list_of_nodes):
    result = []

    for node in list_of_nodes:
        if node.text_type != "text":
            result.append(node)
            continue
        
        link_list = extract_markdown_images(node.text)
        if link_list == []:
            result.append(TextNode(node.text, "text"))
            continue
        text = node.text
        for link in link_list:
            sections = text.split(f"![{link[0]}]({link[1]})", 1)
            if sections[0] != "":
                result.append(TextNode(sections[0], "text"))
            result.append(TextNode(link[0], "image", link[1]))
            
            text = sections[1]
        if text != "":
            result.append(TextNode(text, "text"))
    return result


def split_nodes_link(list_of_nodes):
    result = []
    for node in list_of_nodes:
        if node.text_type != "text":
            result.append(node)
            continue

        link_list = extract_markdown_links(node.text)
        text = node.text
        if link_list == []:
            result.append(TextNode(text, "text"))
            continue
        
        for link in link_list:
            sections = text.split(f"[{link[0]}]({link[1]})", 1)
            if sections[0] != "":
                result.append(TextNode(sections[0], "text"))
            result.append(TextNode(link[0], "link", link[1]))
            text = sections[1]
        if text != "":
            result.append(TextNode(text, "text"))

    return result



def text_to_textnodes(text):
    bold = split_nodes_delimiter([TextNode(text, "text")], "**", "bold")
    italic = split_nodes_delimiter(bold, "*", "italic")
    code = split_nodes_delimiter(italic, "`", "code")

    return split_nodes_link(split_nodes_image(code))