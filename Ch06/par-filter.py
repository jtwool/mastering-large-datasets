from pathos.multiprocessing import ProcessingPool as Pool
from toolz.sandbox.parallel import fold
from functools import reduce


def map_combination(left, right):
  return left + right


def keep_if_even(acc, nxt):
    if nxt % 2 == 0:
        return acc + [nxt]
    else: return acc


with Pool() as P:
    fold(keep_if_even, range(500000), [],
         map=P.imap, combine=map_combination)

print(reduce(keep_if_even, range(500), []))

