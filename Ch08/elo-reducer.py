#! /usr/bin/python3
import json
from sys import stdin
from functools import reduce

def round5(x):
  return 5*int(x/5)

def elo_acc(acc,nxt):
  match_info = json.loads(nxt)
  w_elo = acc.get(match_info['winner'],1400)
  l_elo = acc.get(match_info['loser'],1400)
  Qw = 10**(w_elo/400)
  Ql = 10**(l_elo/400)
  Qt = Qw+Ql
  acc[match_info['winner']] = round5(w_elo + 100*(1-(Qw/Qt)))
  acc[match_info['loser']] = round5(l_elo - 100*(Ql/Qt))
  return acc

if __name__ == "__main__":
  xs = reduce(elo_acc, stdin, {})
  for player, rtg in xs.items():
      print(rtg, player)
