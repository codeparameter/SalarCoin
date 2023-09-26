@classmethod
def sk(cls, sk):
    sk_obj = sk if isinstance(sk, SigningKey) else key_from_string(SigningKey, sk)
    sk = cls('Private Key')
    sk.obj = sk_obj
    sk.h = codecs.encode(sk.obj.to_string(), 'hex')
    sk.b = codecs.decode(sk.h, 'hex')
    sk.b58 = base58.b58encode(sk.b)
    return sk
