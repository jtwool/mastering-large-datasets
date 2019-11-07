from time import clock, sleep
from multiprocessing import Pool


def times_two(x):
  return x*2+7


def lazy_map(xs):
  return list(map(times_two, xs))


def parallel_map(xs, chunck=8500):
  with Pool(2) as P:
    x =  P.map(times_two, xs, chunck)
  return x


for i in range(0, 7):
  N = 10**i
  t1 = clock()
  lazy_map(range(N))
  lm_time = clock() - t1

  t1 = clock()
  parallel_map(range(N))
  par_time = clock() - t1
  print("""
-- N = {} --
Lazy map time:      {}
Parallel map time:  {}
""".format(N, lm_time, par_time))
