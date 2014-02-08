envparse - Parse environment variables instead of arguments
===========================================================

Usage example:

```python
p = envparse.EnvParser('test')
p.add_env('INT', type=int)
p.add_env('INT_LIST', type=envparse.csv(int))
p.add_env('STRING')

env = p.parse(dict(
    INT='1',
    INT_LIST='1,2,3',
    STRING='hello',
))

assert env.INT == 1
assert env.INT_LIST == [1,2,3]
assert env.STRING == 'hello'
```

The full API is:

```
class EnvParser(__builtin__.object)
 |  Methods defined here:
 |
 |  __init__(self, description)
 |
 |  add_env(self, key, type=<type 'str'>, required=True, default=u'')
 |
 |  merge(self, other_env_parser)
 |
 |  parse(self, environ=None)
 |
```

Use the `merge` function to merge two parsers together. That allows
you to define a set of default arguments for reuse in other binaries.

The functions for `type` take one parameter, a string, and return the
according type. They are expected to throw a ValueError if the string
can not be converted.
