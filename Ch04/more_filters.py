from itertools import filterfalse
from toolz.dicttoolz import keyfilter, valfilter, itemfilter

def is_even(x):
    if x % 2 == 0: return True
    else: return False

def both_are_even(x):
    k,v = x
    if is_even(k) and is_even(v): return True
    else: return False

print(list(filterfalse(is_even, range(10))))
# [1, 3, 5, 7, 9]

print(list(keyfilter(is_even, {1:2, 2:3, 3:4, 4:5, 5:6})))
# [2, 4]

print(list(valfilter(is_even, {1:2, 2:3, 3:4, 4:5, 5:6})))
# [1, 3, 5]

print(list(itemfilter(both_are_even, {1:5, 2:4, 3:3, 4:2, 5:1})))
# [2, 4]
