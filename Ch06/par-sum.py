from pathos.multiprocessing import ProcessingPool as Pool
from toolz.sandbox.parallel import fold
from functools import reduce


def my_add(left, right):
  return left+right


with Pool() as P: 
    fold(my_add, range(500000), map=P.imap)

print(reduce(my_add, range(500)))