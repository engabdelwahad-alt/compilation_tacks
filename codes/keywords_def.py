# Automaton for KEYWORDS (letter by letter, keeping the keywords still possible)

KEYWORDS = ["if", "else", "while", "int", "float","for"]


def is_keyword(word):
    if word == "":
        return False

    candidates = KEYWORDS[:]     
    state = 0
    # Loop 1: read the word letter by letter
    for i in range(len(word)):
        letter = word[i]
        new_candidates = []

        # Loop 2: compare this letter with the keywords still possible
        for kw in candidates:
            if i < len(kw) and kw[i] == letter:
                new_candidates.append(kw)

        # No keyword accepts this letter -> rejected state
        if new_candidates == []:
            return False

        # Transition from q(state) to q(state + 1)
        candidates = new_candidates
        state = state + 1

    # End of word: final state only if the word is exactly a keyword
    for kw in candidates:
        if kw == word:
            return True
    return False