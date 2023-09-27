import codecs
import hashlib
import base58
# noinspection PyProtectedMember
from ecdsa import SigningKey

from dependencies.ktools import key_from_string


class KeyObject:

    def __init__(self):
        self._obj = None
        self._b = b''
        self._h = codecs.encode(b'', 'hex')
        self._58 = base58.b58encode(b'')

    def __eq__(self, other: 'KeyObject'):
        if id(self) == id(other):
            return True
        if not isinstance(other, KeyObject):
            return False
        return self.name == other.name and \
               self._obj == other._obj and \
               self._b == other._b and \
               self._58 == other._58

    def get_obj(self):
        return self._obj

    def set_obj(self, _obj):
        self._obj = _obj

    def del_obj(self):
        del self._obj

    obj = property(get_obj, set_obj, del_obj)

    def get_b(self):
        return self._b

    def set_b(self, _b):
        self._b = _b

    def del_b(self):
        del self._b

    b = property(get_b, set_b, del_b)

    def get_h(self):
        return self._h

    def set_h(self, _h):
        self._h = _h

    def del_h(self):
        del self._h

    h = property(get_h, set_h, del_h)

    def get_58(self):
        return self._58

    def set_58(self, _58):
        self._58 = _58

    def del_58(self):
        del self._58

    b58 = property(get_58, set_58, del_58)

    def __repr__(self):
        return str(self)
