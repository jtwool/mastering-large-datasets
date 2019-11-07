from mrjob.job import MRJob
from functools import reduce

def make_counts(acc, nxt):
    acc[nxt] = acc.get(nxt,0) + 1
    return acc

def my_frequencies(xs):
    return reduce(make_counts, xs, {})

class SerenaCounter(MRJob):

  def mapper(self, _, line):
    fields = line.split(',')
    if fields[10] == 'Serena Williams':
        yield fields[2], 'W'
    elif fields[20] == 'Serena Williams':
        yield fields[2], 'L'

  def reducer(self, surface, results):
    counts = my_frequencies(results)
    yield surface, counts

if __name__ == "__main__":
  SerenaCounter.run()
