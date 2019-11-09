from mrjob.job import MRJob

class ErrorCounter(MRJob):
  def mapper(self, _, line):
    fields = line.split(',')
    if fields[7] == '404.0':
      yield fields[6], 1

  def reducer(self, key, vals):
    num_404s = sum(vals)
    if num_404s>0:
      yield key, num_404s

if __name__ == "__main__":
  ErrorCounter.run()

