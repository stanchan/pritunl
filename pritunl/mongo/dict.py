from pritunl.constants import *
from pritunl.exceptions import *
from pritunl.descriptors import *

import abc

class DictMeta(abc.ABCMeta):
    def __instancecheck__(cls, other):
        if isinstance(other, dict):
            return True
        return False

class MongoDict(object):
    __class__ = dict

    def __init__(self, initdict=None, changed=True):
        if initdict is None:
            self.data = None
        elif hasattr(initdict, 'data'):
            self.data = initdict.data
        else:
            self.data = initdict
        self.changed = changed

    def __repr__(self):
        return repr(self.data)

    def __cmp__(self, dict):
        if isinstance(dict, UserDict):
            return cmp(self.data, dict.data)
        else:
            return cmp(self.data, dict)

    __hash__ = None # Avoid Py3k warning

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        if hasattr(self.__class__, "__missing__"):
            return self.__class__.__missing__(self, key)
        raise KeyError(key)

    def __setitem__(self, key, item):
        self.changed = True
        self.data[key] = item

    def __delitem__(self, key):
        self.changed = True
        del self.data[key]

    def clear(self):
        self.changed = True
        self.data.clear()

    def copy(self):
        if self.__class__ is UserDict:
            return UserDict(self.data.copy())
        import copy
        data = self.data
        try:
            self.data = {}
            c = copy.copy(self)
        finally:
            self.data = data
        c.update(self)
        return c

    def keys(self):
        return self.data.keys()

    def items(self):
        return self.data.items()

    def iteritems(self):
        return self.data.iteritems()

    def iterkeys(self):
        return self.data.iterkeys()

    def itervalues(self):
        return self.data.itervalues()

    def values(self):
        return self.data.values()

    def has_key(self, key):
        return key in self.data

    def update(self, dict=None, **kwargs):
        self.changed = True
        if dict is None:
            pass
        elif isinstance(dict, UserDict):
            self.data.update(dict.data)
        elif isinstance(dict, type({})) or not hasattr(dict, 'items'):
            self.data.update(dict)
        else:
            for k, v in dict.items():
                self[k] = v
        if len(kwargs):
            self.data.update(kwargs)

    def get(self, key, failobj=None):
        if key not in self:
            return failobj
        return self[key]

    def setdefault(self, key, failobj=None):
        self.changed = True
        if key not in self:
            self[key] = failobj
        return self[key]

    def pop(self, key, *args):
        self.changed = True
        return self.data.pop(key, *args)

    def popitem(self):
        self.changed = True
        return self.data.popitem()

    def __contains__(self, key):
        return key in self.data

    @classmethod
    def fromkeys(cls, iterable, value=None):
        d = cls()
        for key in iterable:
            d[key] = value
        return d
