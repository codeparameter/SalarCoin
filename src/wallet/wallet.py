from .keyobject import *


# example:
# rawPubKey =
# 'a885dc5c01fd8306097774c81fda64043befea1df2bea01029170c6612e458e4f86333a46e71da57cfe8df8552ddc464081e7139e9084f430668a18d695f636c'
# rawSevretKey = '0048a315d7410cb2d9d33567c19e9943410ba27471e3f08dfabe5a952e626421'
# message = 'Test me'
# signature =
# 'aaa3dad8b884d58dc097e05cf3c4521fe942b19ed39dafb5b840eb8091a902e9e01756e1b5909538e32dc7d0d57e258927014d2fd038b0bcf752042a6579ad4e'


class Wallet:

    def __init__(self, sk):
        if not isinstance(sk, SigningKey):
            sk = key_from_string(SigningKey, sk)
        self.sk = KeyObject.sk(sk)
        self.pk = KeyObject.pk_from_sk(sk)
        self.adr = KeyObject.adr(self.pk)

    def __str__(self):
        return str(self.pk) + str(self.adr) + str(self.sk)

    def __repr__(self):
        return str(self)
