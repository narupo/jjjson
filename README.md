# jjjson

JSON parser made by Python.

```
import jjjson

d = jjjson.parse('{ "word": "how do you do?" }')
print(d)
# {'word': 'how do you do?'}
```

This JSON parser has lazy mode.

```
jjjson.parse(text, lazy=True)
```

A lazy mode allow last-comma, and single-quote-string.
