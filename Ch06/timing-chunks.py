from time import clock
from multiprocessing import Pool


def times_two(x):
  return x*2+7


def parallel_map(xs, chunk_size=8500):
  with Pool(2) as P:
    x = P.map(times_two, xs, chunk_size)
  return x


print("""
{:<10}  |  {}
-------------------------""".format("chunksize", "runtime"))

for i in range(0, 9):
  N = 1000000
  chunk_size = 5 * (10**i)

  t1 = clock()
  parallel_map(range(N), chunk_size)
  parallel_time = clock() - t1

  print("{:<10}  {:>0.3f}".format(chunk_size, parallel_time))
