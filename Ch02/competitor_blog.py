from datetime import date
from urllib import request
from toolz import take


def days_between(start, stop):
    today = date(*start)
    stop = date(*stop)
    while today < stop:
      yield "http://jtwolohan.com/evilblog/"+today.strftime("%m-%d-%Y")
      today = date.fromordinal(today.toordinal()+1)


def get_url(path):
  return request.urlopen(path).read()


if __name__ == "__main__":
    start = (2000, 1, 1)
    stop = (2001, 1, 1)
    xs = map(get_url, days_between(start,stop))
    print(take(5,xs))
