from datetime import date
from urllib import request

from multiprocessing import Pool

def days_between(start,stop):
  today = date(*start)
  stop = date(*stop)
  while today < stop:
    datestr = today.strftime("%m-%d-%Y")
    yield "http://jtwolohan.com/arch-rival-blog/"+datestr
    today = date.fromordinal(today.toordinal()+1)

def get_url(path):
  return request.urlopen(path).read()


with Pool() as P:
  blog_posts = P.map(get_url,days_between((2000,1,1),(2011,1,1)))
