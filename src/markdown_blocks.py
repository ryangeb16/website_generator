

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    block_list = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:
            block_list.append(stripped_block)
    return block_list
