# Automaton for OPERATORS and ASSIGNMENT
#
#   q0 --+ - * /--> q1 (FINAL : OPERATOR)
#   q0 --< >-----> q2 (FINAL : OPERATOR)      q2 --=--> q5
#   q0 --=-------> q3 (FINAL : ASSIGNMENT)    q3 --=--> q5
#   q0 --!-------> q4 (not final)             q4 --=--> q5
#   q5 (FINAL : OPERATOR)  ->  ==  !=  <=  >=

TRANSITIONS = {
    0: {"+": 1, "-": 1, "*": 1, "/": 1, "<": 2, ">": 2, "=": 3, "!": 4},
    2: {"=": 5},
    3: {"=": 5},
    4: {"=": 5},
}

FINALS = {1: "OPERATOR", 2: "OPERATOR", 3: "ASSIGNMENT", 5: "OPERATOR"}


def read_operator(text, pos):
    """Return (end_position, type). If nothing is recognized: (pos, "")."""
    state = 0
    last_final = -1
    last_type = ""
    i = pos

    while i < len(text):
        c = text[i]
        if state in TRANSITIONS and c in TRANSITIONS[state]:
            state = TRANSITIONS[state][c]
        else:
            break
        if state in FINALS:
            last_final = i + 1
            last_type = FINALS[state]
        i = i + 1

    if last_final == -1:
        return pos, ""
    return last_final, last_type

SEPARATORS = ";,(){}"


def read_separator(text, pos):
    """Return the end position (== pos if nothing was recognized)."""
    if pos < len(text) and text[pos] in SEPARATORS:
        return pos + 1          # q0 -> q1 (final)
    return pos
