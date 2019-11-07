from mrjob.job import MRJob
from functools import reduce

def make_counts(acc, nxt):
    acc[nxt] = acc.get(nxt,0) + 1
    return acc

def my_frequencies(xs):
    return reduce(make_counts, xs, {})

class WilliamsRivalry(MRJob):

  def mapper(self, _, line):
    fields = line.split(',')
    players = ' '.join([fields[10], fields[20]])
    if 'Serena Williams' in players and 'Venus Williams' in players:
      yield fields[2], fields[10]

  def reducer(self, surface, results):
    counts = my_frequencies(results)
    yield surface, counts

if __name__ == "__main__":
  WilliamsRivalry.run()
