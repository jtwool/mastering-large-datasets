import re
from toolz.functoolz import pipe, compose

sample_messages = [
"7his所is家4没s4mpl3动m3ss463",
"don7家73ll经4nyon3法7his现m3ss463",
"w3现4r3当b3in6进so好s3cr3t",
"733小h33成h33去nobody看is天on分7o理us",
"w3么will面n3v3r分637理c4u6ht",
"w3事4r3经such没sn34ky天h4ckers"]


def replace_7t(s):
    return s.replace('7', 't')


def replace_3e(s):
    return s.replace('3', 'e')


def replace_6g(s):
    return s.replace('6', 'g')


def replace_4a(s):
    return s.replace('4', 'a')


class chinese_matcher:
    def __init__(self):
        self.r = re.compile(r'[\u4e00-\u9fff]+')
        
    def sub_chinese(self,s):
        return self.r.sub(" ",s)


if __name__ == "__main__":
    C = chinese_matcher()

    # Not chained
    print(list(
    map( C.sub_chinese,
        map(replace_4a,
            map(replace_6g,
                map(replace_3e,
                    map(replace_7t, sample_messages)))))),end="\n\n")

    # Option 1
    hacker_translate = compose(C.sub_chinese, replace_4a, replace_6g,
                               replace_3e, replace_7t)

    print(list(map(hacker_translate, sample_messages)),end="\n\n")

    # Option 2
    def hacker_translate(s):
        return pipe(s, replace_7t, replace_3e, replace_6g,
                       replace_4a, C.sub_chinese)

    print(list(map(hacker_translate,sample_messages)),end="\n\n")
