from jjjson.tokenizer import Tokenizer
from jjjson.parser import Parser


def parse(text, lazy=False):
    t = Tokenizer(lazy=lazy)
    p = Parser(lazy=lazy)
    toks = t.tokenize(text)
    return p.parse(list(toks))
