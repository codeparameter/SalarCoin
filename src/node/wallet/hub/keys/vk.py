@classmethod
def pk_from_sk(cls, sk_obj: SigningKey):
    pk = KeyObject('Public Key')
    pk.obj = sk_obj.verifying_key
    pk.h = codecs.encode(pk.obj.to_string(), 'hex')
    pk.b = codecs.decode(pk.h, 'hex')
    pk.b58 = base58.b58encode(pk.b)
    return pk
