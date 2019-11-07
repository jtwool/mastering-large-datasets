#! /usr/bin/env python3
import re, json
from pyspark import SparkContext

def round5(x):
  return 5*int(x/5)

def clean_match(match):
  ms = match.split(',')
  match_data = {'winner': ms[10],
                'loser': ms[20],
                'surface': ms[2]}
  return match_data

def elo_acc(acc,nxt):
    w_elo = acc.get(nxt['winner'],1600)
    l_elo = acc.get(nxt['loser'],1600)
    Qw = 10**(w_elo/400)
    Ql = 10**(l_elo/400)
    Qt = Qw+Ql
    acc[nxt['winner']] = round5(w_elo + 25*(1-(Qw/Qt)))
    acc[nxt['loser']] = round5(l_elo - 25*(Ql/Qt))
    return acc

def elo_comb(a,b):
    a.update(b)
    return a

if __name__ == "__main__":
  sc = SparkContext(appName="TennisRatings")
  text_files = sc.textFile("/path/to/my/data/wta_matches*")
  xs = text_files.map(clean_match)\
                 .aggregate({},elo_acc, elo_comb)

  for x in sorted(xs.items(), key=lambda x:x[1], reverse=True)[:20]:
      print("{:<30}{}".format(*x))
