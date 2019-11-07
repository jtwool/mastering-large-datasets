#!/usr/bin/env python3

import sys

for line in sys.stdin:
  for word in line.split():
    if len(word) > 6:
      print(word)
