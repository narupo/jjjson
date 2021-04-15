import unittest
import jjjson


class Test(unittest.TestCase):
    def test_parse(self):
        s = '''
'''
        d = jjjson.parse(s)
        self.assertEqual(d, None)

        s = '''
[]
'''
        l = jjjson.parse(s)
        self.assertEqual(len(l), 0)

        s = '''
[1, 2, 3]
'''
        l = jjjson.parse(s)
        self.assertEqual(len(l), 3)
        self.assertEqual(l[0], 1)
        self.assertEqual(l[1], 2)
        self.assertEqual(l[2], 3)

        s = '''
{}
'''
        d = jjjson.parse(s)
        self.assertEqual(len(d), 0)

        s = '''
{
    "a": 1
}
'''
        d = jjjson.parse(s)
        self.assertEqual(d['a'], 1)

        s = '''
{
    "a": 1,
    "b": "BBB"
}
'''
        d = jjjson.parse(s)
        self.assertEqual(d['a'], 1)
        self.assertEqual(d['b'], 'BBB')

        s = '''
{
    "a": 1,
    "b": "BBB",
    "c": [1, 2, 3]
}
'''
        d = jjjson.parse(s)
        self.assertEqual(d['a'], 1)
        self.assertEqual(d['b'], 'BBB')
        self.assertEqual(d['c'], [1, 2, 3])

        s = '''
{
    "a": 1,
    "b": "BBB",
    "c": [1, 2, 3],
    "d": {
        "A": 10,
        "B": "BBBBBB",
        "C": [10, 20, 30]
    }
}
'''
        d = jjjson.parse(s)
        self.assertEqual(d['a'], 1)
        self.assertEqual(d['b'], 'BBB')
        self.assertEqual(d['c'], [1, 2, 3])
        self.assertEqual(d['d']['A'], 10)
        self.assertEqual(d['d']['B'], 'BBBBBB')
        self.assertEqual(d['d']['C'], [10, 20, 30])

        s = '''
{
    "b": "BBB",
    "a": 1,
    "d": {
        "A": 10,
        "B": "BBBBBB",
        "C": [10, 20, 30]
    },
    "c": [1, 2, 3]
}
'''
        d = jjjson.parse(s)
        self.assertEqual(d['a'], 1)
        self.assertEqual(d['b'], 'BBB')
        self.assertEqual(d['c'], [1, 2, 3])
        self.assertEqual(d['d']['A'], 10)
        self.assertEqual(d['d']['B'], 'BBBBBB')
        self.assertEqual(d['d']['C'], [10, 20, 30])

        s = '''
{
    "d": {
        "A": 10,
        "B": "BBBBBB",
        "C": [10, 20, 30]
    },
    "a": 1,
    "c": [1, 2, 3],
    "b": "BBB"
}
'''
        d = jjjson.parse(s)
        self.assertEqual(d['a'], 1)
        self.assertEqual(d['b'], 'BBB')
        self.assertEqual(d['c'], [1, 2, 3])
        self.assertEqual(d['d']['A'], 10)
        self.assertEqual(d['d']['B'], 'BBBBBB')
        self.assertEqual(d['d']['C'], [10, 20, 30])

        s = '''
{
    "d": {
        "A": 10,
        "B": "BBBBBB",
        "C": [10, 20, 30]
    },
    "a": 1,
    "c": [1, 2, 3],
    "b": "BBB"
}
'''
        d = jjjson.parse(s)
        self.assertEqual(d['a'], 1)
        self.assertEqual(d['b'], 'BBB')
        self.assertEqual(d['c'], [1, 2, 3])
        self.assertEqual(d['d']['A'], 10)
        self.assertEqual(d['d']['B'], 'BBBBBB')
        self.assertEqual(d['d']['C'], [10, 20, 30])

        s = '''
{
    "a": 1,
    "b": 3.14
}
'''
        d = jjjson.parse(s)
        self.assertEqual(d['a'], 1)
        self.assertEqual(d['b'], 3.14)

    def test_lazy(self):
        s = '''
{
    'a': 3.14,
}
'''
        d = jjjson.parse(s, lazy=True)
        self.assertEqual(d['a'], 3.14)

        s = '''
{
    'a': 3.14,
    "b": 1,
}
'''
        d = jjjson.parse(s, lazy=True)
        self.assertEqual(d['a'], 3.14)
        self.assertEqual(d['b'], 1)

    def test_syntax_error(self):
        s = '''
{
    "a": 1,
    "b": "BBB"
    "c": [1, 2, 3]
}
'''
        with self.assertRaises(SyntaxError):
            d = jjjson.parse(s)

        s = '''
{
    "a
    ": 1
}
'''
        with self.assertRaises(SyntaxError):
            d = jjjson.parse(s)

        s = '''
{
    "a": 1,
}
'''
        with self.assertRaises(SyntaxError):
            d = jjjson.parse(s)

        s = '''
{}a
'''
        with self.assertRaises(SyntaxError):
            d = jjjson.parse(s)

        s = '''
{
    "a": 123.45.67
}
'''
        with self.assertRaises(SyntaxError):
            d = jjjson.parse(s)

