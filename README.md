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
