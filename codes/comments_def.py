def read_comment(text, pos):
    """Return the end position (== pos if there is no comment here)."""
    state = 0
    i = pos

    while i < len(text):
        c = text[i]
        if state == 0 and c == "/":
            state = 1
        elif state == 1 and c == "/":
            state = 2
        elif state == 2 and c != "\n":
            state = 2
        else:
            break
        i = i + 1

    if state == 2:
        return i
    return pos                  