from pathos.multiprocessing import ProcessingPool as Pool
from toolz.sandbox.parallel import fold
from random import choice
from functools import reduce


def combine_counts(left, right):
  unique_keys = set(left.keys()).union(set(right.keys()))
  return {k:left.get(k, 0)+right.get(k, 0) for k in unique_keys}


def make_counts(acc, nxt):
    acc[nxt] = acc.get(nxt,0) + 1
    return acc


xs = (choice([1, 2, 3, 4, 5, 6]) for _ in range(500000))

with Pool() as P:
    fold(make_counts, xs, {},
         map=P.imap, combine=combine_counts)

print(reduce(make_counts, (choice([1, 2, 3, 4, 5, 6]) for _ in range(500)), {}))
