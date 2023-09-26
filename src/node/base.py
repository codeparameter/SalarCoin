import hashlib
import json

# noinspection PyProtectedMember
from ecdsa import SECP256k1, SigningKey
from dependencies.tools import fake_ip
from src.node.wallet import Wallet
from src.node.wallet import Hub


def neighbors_from_list(nodes: list):
    return {node.adr: node for node in nodes}


class Base(Hub, Wallet):

    def __init__(self, ip, sk):
        Hub.__init__(self, ip)
        Wallet.__init__(self, sk)
        self.neighbors_dict = dict()
        self.neighbors_list = []

    def set_neighbors_list(self):
        self.neighbors_list = [node for node in self.neighbors_dict.values()]

    @classmethod
    def init(cls, ip):
        return cls(ip, SigningKey.generate(curve=SECP256k1, hashfunc=hashlib.sha3_256))

    # factory and seed:

    @classmethod
    def factory(cls):
        return Base.init(fake_ip())

    @staticmethod
    def seeder(amount):
        return [Base.factory() for _ in range(amount)]

    def upcast(self, cls):
        self.__class__ = cls
        return self

    @staticmethod
    def downcast_cls_method(cls, cls_method, *args, **kwargs):
        return getattr(Base, cls_method)(*args, **kwargs).upcast(cls)

    @staticmethod
    def downcast_static_method(cls, static_method, *args, **kwargs):
        return [self.upcast(cls) for self in getattr(Base, static_method)(*args, **kwargs)]

    # neighbor management:

    def add_neighbor(self, node, set_list=True):
        self.neighbors_dict.update(node)
        self.neighbors_dict = self.sort_dict_by_dist(self.neighbors_dict)
        if set_list:
            self.set_neighbors_list()

    def add_neighbors(self, nodes):
        for node in nodes:
            self.add_neighbor(node, set_list=False)
        self.set_neighbors_list()

    # security management:

    def sign_query(self, **data) -> bytes:
        signature = self.sk.obj.sign(json.dumps(data))
        return signature + data + self.pk.h
