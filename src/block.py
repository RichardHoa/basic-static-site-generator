import re


def markdown_to_blocks(markdown):
    blocks = re.split(r"\n\s*\n", markdown.strip())
    return blocks


def block_to_block_type(single_block_markdown):
    character = single_block_markdown.split()
    lines = single_block_markdown.split("\n")
    count = 0
    item_set = set()
    counter_ordererd_list = 1

    if character[0].startswith("#"):
        return "heading"
    if len(character[0].split("```")) == 2 and len(character[-1].split("```")) == 2:
        return "code"
    for line in lines:
        count += 1
        if line.startswith(">"):
            item_set.add("quote")
        elif line.startswith("* ") or line.startswith("- "):
            item_set.add("unordered_list")
        elif line.startswith(f"{counter_ordererd_list}. "):
            counter_ordererd_list += 1
            item_set.add("ordered_list")
        else:
            count -= 1

    if count == len(lines) and len(item_set) == 1:
        return item_set.pop()

    return "paragraph"
