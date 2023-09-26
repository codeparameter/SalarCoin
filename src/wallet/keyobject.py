import codecs
import hashlib
import base58
import string
# noinspection PyProtectedMember
from ecdsa import SigningKey, VerifyingKey, SECP256k1


# example:
# rawPubKey =
# 'a885dc5c01fd8306097774c81fda64043befea1df2bea01029170c6612e458e4f86333a46e71da57cfe8df8552ddc464081e7139e9084f430668a18d695f636c'
# rawSevretKey = '0048a315d7410cb2d9d33567c19e9943410ba27471e3f08dfabe5a952e626421'
# message = 'Test me'
# signature =
# 'aaa3dad8b884d58dc097e05cf3c4521fe942b19ed39dafb5b840eb8091a902e9e01756e1b5909538e32dc7d0d57e258927014d2fd038b0bcf752042a6579ad4e'


def is_hex(s: str) -> bool:
    return all(c in string.hexdigits for c in s)


def checked_hex(key_hex: str, err='must enter a hexa decimal number') -> bytes:
    assert is_hex(key_hex), err
    return bytes.fromhex(key_hex)


def key_from_string(key_type, key_hex: str) -> SigningKey | VerifyingKey:
    key_hex = checked_hex(key_hex)
    return key_type.from_string(key_hex, curve=SECP256k1, hashfunc=hashlib.sha3_256)


# noinspection PyBroadException
def verify(vk, sig, msg):
    try:
        return vk.verify(sig, msg)
    except Exception:
        return False


class KeyObject:

    def __init__(self, name=''):
        self.name = name
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

    def __str__(self):
        return '*' * 20 + \
               f'\n{self.name}:\nbite: {self._b}\nhex: {self._h}\nbase58: {self._58}\n' + \
               '*' * 20 + '\n'

    def __repr__(self):
        return str(self)

    @classmethod
    def sk(cls, sk_obj: SigningKey):
        sk = cls('Private Key')
        sk.obj = sk_obj
        sk.h = codecs.encode(sk.obj.to_string(), 'hex')
        sk.b = codecs.decode(sk.h, 'hex')
        sk.b58 = base58.b58encode(sk.b)
        return sk

    @classmethod
    def pk_from_sk(cls, sk_obj: SigningKey):
        pk = KeyObject('Public Key')
        pk.obj = sk_obj.verifying_key
        pk.h = codecs.encode(pk.obj.to_string(), 'hex')
        pk.b = codecs.decode(pk.h, 'hex')
        pk.b58 = base58.b58encode(pk.b)
        return pk

    @classmethod
    def adr(cls, pk: 'KeyObject'):
        adr = KeyObject('Public Address')
        # getting address from public key
        # Run SHA-256 for the public key
        sha256_bpk = hashlib.sha256(pk.b)
        sha256_bpk_digest = sha256_bpk.digest()
        # Run RIPEMD-160 for the SHA-256
        ripemd160_bpk = hashlib.new('ripemd160')
        ripemd160_bpk.update(sha256_bpk_digest)
        ripemd160_bpk_digest = ripemd160_bpk.digest()
        ripemd160_bpk_hex = codecs.encode(ripemd160_bpk_digest, 'hex')

        network_public_key_bytes = b'00' + ripemd160_bpk_hex

        # Double SHA256 to get checksum
        sha256_net_bpk = hashlib.sha256(network_public_key_bytes)
        sha256_net_bpk_digest = sha256_net_bpk.digest()
        sha256_2_net_bpk = hashlib.sha256(sha256_net_bpk_digest)
        sha256_2_net_bpk_digest = sha256_2_net_bpk.digest()
        sha256_2_hex = codecs.encode(sha256_2_net_bpk_digest, 'hex')
        checksum = sha256_2_hex[:8]

        adr.h = network_public_key_bytes + checksum
        adr.b = codecs.decode(adr.h, 'hex')
        adr.b58 = base58.b58encode(adr.b)
