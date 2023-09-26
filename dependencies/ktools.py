import hashlib

from ecdsa import SECP256k1, SigningKey, VerifyingKey

from dependencies.tools import checked_hex


def key_from_string(key_type, key_hex: str) -> SigningKey | VerifyingKey:
    key_hex = checked_hex(key_hex)
    return key_type.from_string(key_hex, curve=SECP256k1, hashfunc=hashlib.sha3_256)


# noinspection PyBroadException
def verify(vk, sig, msg):
    try:
        return vk.verify(sig, msg)
    except Exception:
        return False
