
def is_letter(c):
    return "a" <= c <= "z" or "A" <= c <= "Z"

def is_digit(c):
    return "0" <= c <= "9"

def read_identifier(text, pos):
    """Read an identifier starting at position pos.
    Return the end position (== pos if nothing was recognized)."""
    # Transition from q0 to q1
    if pos >= len(text) or not (is_letter(text[pos]) or text[pos] == "_"):
        return pos

    i = pos + 1
    # Remain in accepting state q1
    while i < len(text) and (is_letter(text[i]) or is_digit(text[i]) or text[i] == "_"):
        i = i + 1
    return i