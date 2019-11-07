words = ["apple","mongoose","walk","mouse","good",
         "pineapple","yeti","minnesota","mars",
         "phone","cream","cucumber","coffee","elementary",
         "sinister","science","empire"]

def contains_m(s):
    if "m" in s.lower(): return True
    else: return False

m_words = filter(contains_m, words)

next(m_words)
next(m_words)
next(m_words)

print(list(m_words))
# [“mars”,”cream”,”cucumber”,”elementary”, ... ]
