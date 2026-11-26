# this for lexical analysis of a simple programming language
# re for regular expressions : It allows us to search for patterns inside text.
import re


# Counter counts how many times each element appears : We will use it at the end to calculate token statistics.
from collections import Counter


KEYWORDS = {"if", "else", "while", "int", "float"}

TOKEN_SPECIFICATION = [
    ("COMMENT", r"//[^\n]*"),
    ("NUMBER", r"\d+(\.\d+)?"),
    ("IDENTIFIER", r"[A-Za-z_][A-Za-z0-9_]*"),
    ("OPERATOR", r"==|!=|<=|>=|[+\-*/<>]"),
    ("ASSIGNMENT", r"="),
    ("SEPARATOR", r"[;,(){}]"),
    ("WHITESPACE", r"\s+"),
    ("INVALID", r"."),
]


def lexical_analysis(source_code):
    tokens = []
    errors = []

    pattern = "|".join(
        # It is a named capturing group in regular expressions.
        f"(?P<{name}>{regex})"
        for name, regex in TOKEN_SPECIFICATION
    )

    line = 1
    column = 1

    for match in re.finditer(pattern, source_code):
        token_type = match.lastgroup
        lexeme = match.group()

        # Save the starting position of this match
        start_line = line
        start_column = column

        # Ignore comments and whitespace
        if token_type not in ("COMMENT", "WHITESPACE"):

            if token_type == "INVALID":
                errors.append(
                    f"Lexical error: {lexeme!r} "
                    f"at line {start_line}, column {start_column}"
                )

            else:
                # Classify keywords
                if token_type == "IDENTIFIER" and lexeme in KEYWORDS:
                    token_type = "KEYWORD"

                # Distinguish integer and real numbers
                if token_type == "NUMBER":
                    if "." in lexeme:
                        token_type = "REAL"
                    else:
                        token_type = "INTEGER"

                # Store token type, lexeme, and line number
                tokens.append((token_type, lexeme, start_line))

        # Update line and column positions
        if "\n" in lexeme:
            line += lexeme.count("\n")
            column = len(lexeme.rsplit("\n", 1)[-1]) + 1
        else:
            column += len(lexeme)

    # Count tokens of each type
    statistics = Counter(token[0] for token in tokens)

    return tokens, errors, statistics


# Example input
# source = """int x = 10;
#  // initialize x
#  print('x');
# float y = 2.5;"""
source = input("Enter source code: ")

tokens, errors, statistics = lexical_analysis(source)

print("TOKENS:")
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

for token_type, count in sorted(statistics.items()):
    print(f"{token_type}: {count}")