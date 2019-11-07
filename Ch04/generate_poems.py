import re, os, glob
from functools import reduce
from random import randint, choice
from multiprocessing import Pool
from math import floor

class ContentMatcher:
    def __init__(self):
        self.r = re.compile(r'[A-Z\W-]+')
    def is_content(self,l):
        if self.r.fullmatch(l):
            return False
        else: return True

def line_to_thirds(l):
  words = l.split()
  n = len(words)
  breakpoint = floor(n / 3)
  return {"first": " ".join(words[:breakpoint]),
         "second": " ".join(words[breakpoint:breakpoint*2]),
         "third": " ".join(words[breakpoint*2:])}

def join_breaks(acc,nxt):
    return {k:v+[nxt[k]] for k,v in acc.items()}

def consolidate_content(fp,R):
    with open(fp) as f:
        with Pool() as P:
            content = P.map(line_to_thirds, filter(R.is_content, f.readlines()))
    return reduce(join_breaks,
                  content,
                  {"first":[],"second":[],"third":[]})

def make_line(parts):
    return " ".join([choice(parts['first']),
                    choice(parts["second"]),
                    choice(parts["third"])])

def write_poem(parts,name,i):
    fp = "{}/poem_{}.txt".format(name,i)
    num_lines = randint(7,40)
    lines = (make_line(parts) for _ in range(num_lines))
    with open(fp,"w") as f:
        f.write("\n".join(lines))

def calc_total_size():
    paths = glob.iglob("./author*/*")
    return sum(map(os.path.getsize,paths))

def generate_poems(a, b, max_size=10000000):
    try:
        os.mkdir("author_a")
        os.mkdir("author_b")
    except FileExistsError:
        pass
    i = 1
    #while calc_total_size() < max_size:
    for _ in range(floor(max_size/1000)):
        write_poem(a,"author_a",i)
        write_poem(b,"author_b",i)
        i+=1

if __name__ == "__main__":
    CM = ContentMatcher()
    author_a = consolidate_content("A.txt",CM)
    author_b = consolidate_content("B.txt",CM)
    generate_poems(author_a, author_b)
