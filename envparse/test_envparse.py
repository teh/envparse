import pytest
import envparse

def test_parsing():
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


def test_merge():
    p1 = envparse.EnvParser('test')
    p1.add_env('INT', type=int)

    p2 = envparse.EnvParser('test')
    p2.add_env('INT2', type=int)

    p1.merge(p2)

    env = p1.parse(dict(
        INT='1',
        INT2='2',
    ))

    assert env.INT == 1
    assert env.INT2 == 2

def test_broken_merge():
    p1 = envparse.EnvParser('test')
    p1.add_env('INT', type=int)

    p2 = envparse.EnvParser('test')
    p2.add_env('INT', type=int)

    with pytest.raises(envparse.Error):
        p1.merge(p2)
