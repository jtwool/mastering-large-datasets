from functools import reduce

xs = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def keep_if_even(acc, nxt):
    if nxt % 2 == 0:
        return acc + [nxt]
    else:
        return acc


reduce(keep_if_even, xs, [])
