# Lexical analyzer built with AUTOMATA
import sys

from keywords_def import is_keyword
from identifier_def import read_identifier
from numbers_def import read_number
from operator_separator import read_separator,read_operator
from comments_def import read_comment



def lexical_analysis(source):
    tokens = []
    errors = []
    statistics = {}

    pos = 0
    line = 1
    column = 1

    while pos < len(source):
        c = source[pos]

        # ---- whitespace : ignored ----
        if c in " \t\r\n":
            if c == "\n":
                line = line + 1
                column = 1
            else:
                column = column + 1
            pos = pos + 1
            continue

        # ---- 1) comment : ignored ----
        end = read_comment(source, pos)
        if end > pos:
            column = column + (end - pos)
            pos = end
            continue

        # ---- 2) number ----
        end, kind = read_number(source, pos)
        if end > pos:
            tokens.append((kind, source[pos:end], line))
            column = column + (end - pos)
            pos = end
            continue

        # ---- 3) identifier or keyword ----
        end = read_identifier(source, pos)
        if end > pos:
            lexeme = source[pos:end]
            if is_keyword(lexeme):          # keyword automaton
                kind = "KEYWORD"
            else:
                kind = "IDENTIFIER"
            tokens.append((kind, lexeme, line))
            column = column + (end - pos)
            pos = end
            continue

        # ---- 4) operator / assignment ----
        end, kind = read_operator(source, pos)
        if end > pos:
            tokens.append((kind, source[pos:end], line))
            column = column + (end - pos)
            pos = end
            continue

        # ---- 5) separator ----
        end = read_separator(source, pos)
        if end > pos:
            tokens.append(("SEPARATOR", source[pos:end], line))
            column = column + (end - pos)
            pos = end
            continue

        # ---- no automaton accepts this character : lexical error ----
        errors.append(f"Lexical error: {c!r} at line {line}, column {column}")
        column = column + 1
        pos = pos + 1

    # count the tokens of each type
    for token in tokens:
        kind = token[0]
        if kind in statistics:
            statistics[kind] = statistics[kind] + 1
        else:
            statistics[kind] = 1

    return tokens, errors, statistics


# ------------------------------------------------------------
# Get the program from the user
# ------------------------------------------------------------
if len(sys.argv) > 1:
    with open(sys.argv[1], encoding="utf-8") as f:
        source = f.read()
else:
    print("Enter your program (write END on a new line to finish):")
    lines = []
    while True:
        try:
            text = input()
        except EOFError:
            break
        if text.strip() == "END":
            break
        lines.append(text)
    source = "\n".join(lines)

tokens, errors, statistics = lexical_analysis(source)

print("\nTOKENS:")
for token in tokens:
    print(token)

print("\nLEXICAL ERRORS:")
if errors:
    for error in errors:
        print(error)
else:
    print("No lexical errors.")

print("\nTOKEN STATISTICS:")
print("Total tokens:", len(tokens))

for kind, count in sorted(statistics.items()):
    print(f"{kind}: {count}")