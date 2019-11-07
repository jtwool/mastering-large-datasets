#! /usr/bin/env python3
import re
from pyspark import SparkContext

if __name__ == "__main__":
  sc = SparkContext(appName="WordScores")
  PAT = re.compile(r'[-./:\s\xa0]+')
  text_files = sc.textFile("/home/jt-w/Code/MR-test/data/*")
  xs = text_files.flatMap(lambda x:PAT.split(x))\
                 .filter(lambda x:len(x)>6)\
                 .countByValue()\

  for k,v in xs.items():
    print("{:<30}{}".format(k.encode("ascii","ignore"),v))
