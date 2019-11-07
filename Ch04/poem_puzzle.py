import toolz
import re, itertools
from glob import iglob


def word_ratio(d):
    """This helper function returns the ratio of a's to the's"""
    return float(d.get("a",0))/float(d.get("the",0.0001))


class PoemCleaner:
    def __init__(self):
        self.r = re.compile(r'[.,;:!-]')

    def clean_poem(self, fp):
        """This helper function opens a poem at a filepath and returns a clean poem.

        A clean poem will be a punctuation-less sequence of lowercase words, in
        the order that the author of the poem placed them.
        """
        with open(fp) as poem:
            no_punc = self.r.sub("",poem.read())
            return no_punc.lower().split()


def word_is_desired(w):
    """This helper function detects whether a word is "a" or "the".

    It is designed to be used in conjunction with filter to filter a sequence
    of words down to just definite and indefinite articles.
    """
    if w in ["a","the"]:
        return True
    else:
        return False


def analyze_poems(poems, cleaner):
    return word_ratio(
        toolz.frequencies(
            filter(word_is_desired,
                itertools.chain(*map(cleaner.clean_poem, poems)))))


if __name__ == "__main__":

    Cleaner = PoemCleaner()
    author_a_poems = iglob("author_a/*.txt")
    author_b_poems = iglob("author_b/*.txt")

    author_a_ratio = analyze_poems(author_a_poems, Cleaner)
    author_b_ratio = analyze_poems(author_b_poems, Cleaner)

    print("""
    Original_Poem:  0.3
    Author A:     {:.2f}
    Author B:     {:.2f}
    """.format(author_a_ratio, author_b_ratio))
