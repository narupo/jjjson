from absstream.stream import Stream
from jjjson.tokenizer import *


class Parser:
    class Result:
        def __init__(self):
            self.dic = None
            self.lis = None
            self.number = None
            self.string = None
            self.key = None

        def set(self, key, val):
            if key is None or val is None:
                return
            if self.dic is None:
                self.dic = {}
            self.dic[key] = val

        def update(self, d):
            if d is None:
                return
            if self.dic is None:
                self.dic = {}
            self.dic.update(d)

        def append(self, el):
            if el is None:
                return
            if self.lis is None:
                self.lis = []
            self.lis.append(el)

        def get_alive_elem(self):
            if self.dic is not None:
                return self.dic
            elif self.lis is not None:
                return self.lis
            elif self.number is not None:
                return self.number
            elif self.string is not None:
                return self.string
            else:
                return None

    def __init__(self, lazy=False):
        self.lazy = lazy

    def parse(self, toks):
        s = Stream(toks)
        r = Parser.Result()

        self.read_spaces(s)
        if s.eof():
            return r.get_alive_elem()

        self.p_brace_or_bracket(s, r)
        self.read_spaces(s)
        if not s.eof():
            raise SyntaxError('invalid format')

        return r.get_alive_elem()

    def read_spaces(self, s):
        while not s.eof():
            t = s.get()
            if isinstance(t, Spaces):
                pass
            else:
                s.prev()
                break

    def p_brace_or_bracket(self, s, r):
        if s.eof():
            return

        self.read_spaces(s)
        t = s.get()
        if isinstance(t, LeftBrace):
            s.prev()
            return self.p_brace(s, r)
        elif isinstance(t, LeftBracket):
            s.prev()
            return self.p_bracket(s, r)
        else:
            raise SyntaxError('invalid format')

    def p_brace(self, s, r):
        if s.eof():
            return

        self.read_spaces(s)
        t = s.get()
        if not isinstance(t, LeftBrace):
            raise SyntaxError('not found left-brace')

        while not s.eof():
            r2 = Parser.Result()
            self.p_key(s, r2)
            r.set(r2.key, r2.get_alive_elem())

            self.read_spaces(s)
            t = s.get()
            if isinstance(t, Comma):
                self.read_spaces(s)
                if not self.lazy and isinstance(s.cur(), RightBrace):
                    raise SyntaxError('invalid last comma')
            elif isinstance(t, RightBrace):
                if r.dic is None:
                    r.dic = {}
                break
            else:
                raise SyntaxError('invalid dict')

    def p_key(self, s, r):
        if s.eof():
            raise SyntaxError('invalid format')

        self.read_spaces(s)
        t = s.get()
        if isinstance(t, String):
            r.key = t.text
            return self.p_colon(s, r)
        elif isinstance(t, RightBrace):
            s.prev()
            return 
        else:
            raise SyntaxError('not found key')

    def p_colon(self, s, r):
        if s.eof():
            raise SyntaxError('invalid format')

        self.read_spaces(s)
        t = s.get()
        if not isinstance(t, Colon):
            raise SyntaxError('not found colon')

        return self.p_elem(s, r)

    def p_elem(self, s, r):
        if s.eof():
            raise SyntaxError('invalid format')

        self.read_spaces(s)
        t = s.get()
        if isinstance(t, LeftBrace):
            s.prev()
            return self.p_brace(s, r)
        elif isinstance(t, LeftBracket):
            s.prev()
            return self.p_bracket(s, r)
        elif isinstance(t, String):
            s.prev()
            return self.p_string(s, r)
        elif isinstance(t, Number):
            s.prev()
            return self.p_number(s, r)
        else:
            raise SyntaxError('invalid element')

    def p_bracket(self, s, r):
        if s.eof():
            raise SyntaxError('not closed list')

        self.read_spaces(s)
        t = s.get()
        if not isinstance(t, LeftBracket):
            raise RuntimeError('internal error (1)')

        if isinstance(s.cur(), RightBracket):
            s.get()
            r.lis = []
            return

        while not s.eof():
            r2 = Parser.Result()
            self.p_elem(s, r2)
            r.append(r2.get_alive_elem())

            self.read_spaces(s)
            t = s.get()
            if isinstance(t, Comma):
                if not self.lazy and isinstance(s.cur(), RightBracket):
                    raise SyntaxError('invalid last comma')
            elif isinstance(t, RightBracket):
                break
            else:
                raise SyntaxError('invalid list format')

    def p_string(self, s, r):
        if s.eof():
            raise SyntaxError('not found string')

        self.read_spaces(s)
        t = s.get()
        if not isinstance(t, String):
            raise SyntaxError('not found string')

        r.string = t.text

    def p_number(self, s, r):
        if s.eof():
            raise SyntaxError('not found number')

        self.read_spaces(s)
        t = s.get()
        if not isinstance(t, Number):
            raise SyntaxError('not found number')

        if '.' in t.text:
            r.number = float(t.text)
        else:
            r.number = int(t.text)
