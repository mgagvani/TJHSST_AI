# Manav Gagvani
# Ghost (modeling challenge 3)
import sys

BIG = 9999999999999999


def next_letter(word, possibilities):
    letters = {}
    ind = len(word)
    for word in possibilities:
        letters[word[ind]] = letters.get(word[ind], []) + [word]
    return letters


def max_step(word, possibilities, alpha, beta):
    if word in possibilities:
        return 1  # win
    outcomes = []
    next_move = next_letter(word, possibilities)
    for letter in next_move.keys():
        new_word = word + letter
        result = min_step(new_word, next_move[letter], alpha, beta)
        outcomes.append(result)
        if (
            result >= beta
        ):  # if result is greater than or equal to beta, then we can prune
            return result
        if result > alpha:  # if result is greater than alpha, then we can update alpha
            alpha = result
        outcomes.append(result)
    return min(alpha, max(outcomes))


def min_step(word, possibilities, alpha, beta):
    if word in possibilities:
        return -1  # lose
    outcomes = []
    next_move = next_letter(word, possibilities)
    for letter in next_move.keys():
        new_word = word + letter
        outcome = max_step(new_word, next_move[letter], alpha, beta)
        if (
            alpha >= outcome
        ):  # if alpha is greater than or equal to outcome, then we can prune
            return outcome
        if beta > outcome:  # if beta is greater than outcome, then we can update beta
            beta = outcome
        outcomes.append(outcome)
    return max(beta, min(outcomes))


def play_turn(word, possible):
    # print(word)
    guarantee_success = []
    next_move = next_letter(word, possible)
    for letter in next_move.keys():
        new_word = word + letter
        outcome = min_step(
            new_word, next_move[letter], -BIG, BIG
        )  # alpha and beta are arbitrary numbers
        if outcome == 1:  # if outcome is 1, then we can guarantee a win
            guarantee_success.append(letter)
    if len(guarantee_success) > 0:
        print(f"Next player can win by with any of these letters: {guarantee_success}")
        letter = guarantee_success[0]
        new_word = word + letter
    else:
        print("Next player will lose!")


if __name__ == "__main__":
    _len = len
    args = sys.argv
    filename = args[1]
    min_length = int(args[2])

    word = ""
    if _len(args) == 4:
        word = args[3]

    dictionary = []
    with open(filename) as file:
        for line in file:
            line = line.strip().upper()
            if line.isalpha():
                if line.startswith(word) and _len(line) >= min_length:
                    dictionary.append(line)
            # word_length_dict[len(line)]=word_length_dict.get(len(line),[])+[line]
            # the word length dict was unnecessary

    play_turn(word, dictionary)
