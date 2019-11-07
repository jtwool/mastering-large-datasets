#!/usr/bin/env python3

import sys
from functools import reduce

def keep_highest(acc, nxt):
  word, score = nxt.split('\t')
  s = int(score)
  if len(acc) < 5:
    acc.append((word,s))
    acc = sorted(acc, key=lambda x:x[1])
  elif s > acc[0][1]:
    acc.append((word, s))
    acc = sorted(acc, key=lambda x:x[1])[1:]
  return acc

print(reduce(keep_highest, sys.stdin, []))
