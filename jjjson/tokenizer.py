from absstream.stream import Stream


class Token:
    def __init__(self, text=None):
        self.text = text


class Etc(Token):
    pass

class Spaces(Token):
    pass

class LeftBrace(Token):
    pass


class RightBrace(Token):
    pass


class LeftBracket(Token):
    pass


class RightBracket(Token):
    pass


class String(Token):
    pass


class Number(Token):
    pass


class Comma(Token):
    pass


class Colon(Token):
    pass


class Tokenizer:
    def __init__(self, lazy=False):
        self.lazy = lazy

    def tokenize(self, text):
        s = Stream(text)
        buf = ''

        def store_etc():
            nonlocal buf
            if len(buf):
                yield Etc(buf)
                buf = ''

        while not s.eof():
            c1 = s.get()
            if c1 == '{':
                yield from store_etc()
                yield LeftBrace()
            elif c1 == '}':
                yield from store_etc()
                yield RightBrace()
            elif c1 == '[':
                yield from store_etc()
                yield LeftBracket()
            elif c1 == ']':
                yield from store_etc()
                yield RightBracket()
            elif c1 == ':':
                yield from store_etc()
                yield Colon()
            elif c1 == ',':
                yield from store_etc()
                yield Comma()
            elif c1.isspace():
                yield from store_etc()
                s.prev()
                txt = self.read_spaces(s)
                yield Spaces(txt)
            elif c1 == '"':
                yield from store_etc()
                s.prev()
                txt = self.read_dq_string(s)
                yield String(txt)
            elif self.lazy and c1 == "'":
                yield from store_etc()
                s.prev()
                txt = self.read_sq_string(s)
                yield String(txt)
            elif c1.isdigit():
                yield from store_etc()
                s.prev()
                txt = self.read_number(s)
                yield Number(txt)
            else:
                buf += c1

        yield from store_etc()

    def read_spaces(self, s):
        buf = ''

        while not s.eof():
            c = s.get()
            if c.isspace():
                buf += c
            else:
                s.prev()
                break

        return buf

    def read_number(self, s):
        m = 0
        buf = ''

        while not s.eof():
            c = s.get()
            if m == 0:
                if c.isdigit():
                    buf += c
                elif c == '.':
                    buf += c
                    m = 10
                else:
                    s.prev()
                    break
            elif m == 10:
                if c.isdigit():
                    buf += c
                else:
                    s.prev()
                    break

        return buf

    def read_string(self, s, quote='"'):
        c1 = s.get()
        if c1 != quote:
            raise ValueError('invalid character in read-string')

        buf = ''

        while not s.eof():
            c1 = s.get()
            c2 = s.cur()
            if c1 == quote:
                break
            elif (c1 == '\r' and c2 == '\n') or \
                 (c1 == '\r' or c2 == '\n'):
                raise SyntaxError('string literal not allowed newlines')

            buf += c1

        return buf

    def read_dq_string(self, s):
        return self.read_string(s, '"')

    def read_sq_string(self, s):
        return self.read_string(s, "'")

    def is_valid_quote(self, c):
        return c == '"'
