from functools import reduce

xs = [10, 5, 1, 19, 11, 203]


def my_add(acc, nxt):
    return acc + nxt


print(reduce(my_add, xs, 0))

# With a lambda instead:
print(reduce(lambda acc, nxt: acc+nxt, xs, 0))
