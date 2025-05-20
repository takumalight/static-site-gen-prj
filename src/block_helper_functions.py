def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = map(lambda block: block.strip(), blocks)
    blocks = list(filter(lambda block: block != "", blocks))
    return blocks