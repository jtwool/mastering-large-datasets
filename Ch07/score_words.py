#!/usr/bin/env python3

import sys

def score(word):
  total = 0
  for i,char in enumerate(word):
    if char.lower() in "dlcu":
      total +=1
    elif char.lower() in "mwfbygpvk":
      total += 2
    elif char.lower() in "jxqz":
      total += 4
    if i >= 4:
      total +=2
  return total

for line in sys.stdin:
  for word in line.split():
    print("{}\t{}".format(word, score(word)))
