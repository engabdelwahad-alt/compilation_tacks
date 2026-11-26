# Automaton for NUMBERS :  digit+ ( . digit+ )?
#
#   q0 --digit--> q1 (FINAL : INTEGER)
#   q1 --digit--> q1
#   q1 --"."----> q2
#   q2 --digit--> q3 (FINAL : REAL)
#   q3 --digit--> q3
# from utils import is_digit



def is_digit(c):
    return "0" <= c <= "9"

def read_number(text, pos):
    """Read a number starting at position pos.
    Return (end_position, type). If nothing is recognized: (pos, "")."""
    state = 0
    last_final = -1          # end of the longest number accepted so far
    last_type = ""
    i = pos

    while i < len(text):
        c = text[i]
        if state == 0 and is_digit(c):
            state = 1
        elif state == 1 and is_digit(c):
            state = 1
        elif state == 1 and c == ".":
            state = 2
        elif state == 2 and is_digit(c):
            state = 3
        elif state == 3 and is_digit(c):
            state = 3
        else:
            break            # no transition -> stop reading

        if state == 1:
            last_final = i + 1
            last_type = "INTEGER"
        elif state == 3:
            last_final = i + 1
            last_type = "REAL"
        i = i + 1

    if last_final == -1:
        return pos, ""
    return last_final, last_type
