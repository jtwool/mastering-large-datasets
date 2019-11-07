import dill as pickle
from toolz.sandbox.parallel import fold
from pathos.multiprocessing import ProcessingPool as Pool
from random import choice

N = 100000
P = Pool()

# Parallel summation
def my_add(left, right):
  return left+right

xs = range(N)

print(fold(my_add, xs, map=P.imap))

# Parallel filter
def map_combination(left, right):
  return left + right

def keep_if_even(acc, nxt):
    if nxt % 2 == 0:
        return acc + [nxt]
    else: return acc

print(fold(keep_if_even, xs, [], map=P.imap, combine=map_combination))

#Parallel frequencies
def combine_counts(left, right):
  unique_keys = set(left.keys()).union(set(right.keys()))
  return {k:left.get(k,0)+right.get(k,0) for k in unique_keys}

def make_counts(acc, nxt):
    acc[nxt] = acc.get(nxt,0) + 1
    return acc

xs = (choice([1,2,3,4,5,6]) for _ in range(N))

print(fold(make_counts, xs, {}, map=P.imap, combine=combine_counts))
