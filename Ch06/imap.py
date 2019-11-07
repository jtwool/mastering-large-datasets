from multiprocessing import Pool


def increase(x):
  return x+1


with Pool() as P:
  a = P.map(increase, range(100))


with Pool() as P:
  b = P.imap(increase, range(100))


with Pool() as P:
  c = P.imap_unordered(increase, range(100))

print(a)
print(b)
print(c)
