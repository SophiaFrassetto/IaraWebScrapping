def remove_duplicate_char(text: str):
    return "".join([x for i, x in enumerate(text) if i == 0 or text[i-1] != x])