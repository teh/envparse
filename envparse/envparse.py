"""A module to parse environment variables into their correct
types.

Example:

    p = envparse.EnvParser('Port Parser')
    p.add_env('LISTEN_PORT', type=int)
    p.add_env('HOST')

    env = p.parse()

    print("Listening on {}:{}".format(env.HOST, env.LISTEN_PORT))
"""
from __future__ import print_function, unicode_literals, absolute_import, division

import csv as csv_reader
import os
import re
import collections

Key = collections.namedtuple('Key', 'type required default')

class Error(Exception):
    pass


def csv(type_):
    """Expect a comma-seperated list of type_.

    Example:

    parser.add_env('INT_LIST', type=envparse.csv(int))
    print(parser.parse(dict(INT_LIST='1,2,3')))

    """
    def _parse(data):
        entries = csv_reader.reader([data]).next()
        result = []
        for e in entries:
            try:
                result.append(type_(e))
            except ValueError:
                # TODO what error to throw?
                raise
        return result

    return _parse


class EnvParser(object):
    def __init__(self, description):
        self.description = description
        self._keys = dict()

    def add_env(self, key, type=bytes, required=True, default=''):
        if key in self._keys:
            raise Error('Key `{}` already defined.'.format(key))

        if not re.match(r'[A-Za-z_][A-Za-z0-9_]+', key):
            raise Error('Invalid key name `{}`.'.format(key))

        self._keys[key] = Key(type, required, default)

    def parse(self, environ=None):
        if environ is None:
            environ = os.environ

        Env = collections.namedtuple('Env', ' '.join(sorted(self._keys)))
        values = []

        for name, key in sorted(self._keys.items()):
            if key.required and name not in environ:
                raise Error('Key `{}` not found in environment.'.format(name))
            else:
                try:
                    value = key.type(environ.get(name, key.default))
                except ValueError:
                    raise Error('Key `{}` could not be parsed as {}.'.format(name, key.type))

            values.append(value)

        return Env(*values)

    def merge(self, other_env_parser):
        for k, v in other_env_parser._keys.items():
            self.add_env(k, v.type, v.required, v.default)
