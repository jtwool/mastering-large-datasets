from functools import reduce


def score_word(word):
    points = 0
    for char in word:
        if char == "z": points += 10
        elif char in ["f", "h", "v", "w"]: points += 5
        elif char in ["b", "c", "m", "p"]: points += 3
        else: points += 1
    return points


words = ["these", "are", "my", "words"]

total_score = reduce(lambda acc,nxt: acc+nxt, map(score_word, words))
print(total_score)
