from functools import reduce

xs = ["A", "B", "C", "A", "A", "C", "A"]
ys = [1, 3, 6, 1, 2, 9, 3, 12]


def make_counts(acc, nxt):
    acc[nxt] = acc.get(nxt, 0) + 1
    return acc


def my_frequencies(xs):
    return reduce(make_counts, xs, {})


print(my_frequencies(xs))
print(my_frequencies(ys))
print(my_frequencies("mississippi"))
