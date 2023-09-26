import json
import socket
# noinspection PyProtectedMember
from ecdsa import VerifyingKey
from dependencies.ntools import fap, calculate_distance
from dependencies.tools import sort_dict, multi_thread_chain
from src.globals import ROUTES
from src.node.wallet import verify, key_from_string

BUCKETS = 16  # kademlia buckets amount
MAX_NEIGHBORS = 1 + 2 * (BUCKETS - 1)  # 2 node per bucket except the first bucket has 1 node
NODES_PER_SERVER = 5  # choose a number suitable for chucking the response data
CHOSEN_NODES = MAX_NEIGHBORS // NODES_PER_SERVER

BAD_QUERY = b'400:BadQuery'
ROUTE_NOT_FOUND = b'404:RouteNotFound'


def get_verified_query(query: bytes) -> (bool, dict, VerifyingKey):
    if len(query) < 178:
        return False, None, None
    signature = query[:128]
    data = query[128:-50]
    pk = key_from_string(VerifyingKey, query[-50:].decode())
    return verify(pk, signature, data), json.loads(data), pk


class Hub:

    def __init__(self, ip, port=0, adr=None):
        self.ip = ip
        self.port = port if port else next(fap)
        self.adr = adr
        self.tasks = [self.get_requests]

    @classmethod
    def from_dict(cls, d):
        return cls(d['ip'], d['port'], d['adr'])

    @staticmethod
    def from_dicts(dicts: list):
        return [Hub.from_dict(d) for d in dicts]

    def __eq__(self, other: 'Hub'):
        if id(self) == id(other):
            return True
        if not isinstance(other, Hub):
            return False
        return self.adr == other.adr

    # route management:

    @staticmethod
    def sort_by_dist(node1):
        return lambda node2: calculate_distance(node1.ip, node2.ip)

    def sort_list_by_dist(self, others: list):
        return sorted(others, key=Hub.sort_by_dist(self))

    def sort_dict_by_dist(self, others: dict):
        return sort_dict(others, Hub.sort_by_dist(self))

    # network management:

    def router(self, query):
        if 'route' not in query:
            return BAD_QUERY
        route = query['route']
        if route not in ROUTES:
            return ROUTE_NOT_FOUND
        controller, action = ROUTES[route]
        if type(self) != type(controller):
            return ROUTE_NOT_FOUND
        return action

    def get_action(self, query):
        action = self.router(query)
        if action == BAD_QUERY or action == ROUTE_NOT_FOUND:
            return action
        return getattr(self, action)

    # noinspection PyBroadException
    def respond(self, data) -> bytes:
        try:
            (verified, query, vk), (ip, port) = data
            if not verified:
                return BAD_QUERY
            fn = self.get_action(query)
            return fn(query, ip, port)
        except Exception:
            return BAD_QUERY

    def get_requests(self):
        # server_address = (self.ip, self.port)  # commented for the sake of testing purposes
        server_address = ('127.0.0.1', self.port)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(server_address)
        # this connection protocol is TCP, not UDP
        # in blockchain in order to make p2p connections we use TCp
        # just unlike video calls which use UDP
        server_socket.listen(10)

        while True:
            client_socket, client_address = server_socket.accept()
            data = client_socket.recv(1024)
            response = self.respond((get_verified_query(data), client_address))
            client_socket.sendall(response)
            client_socket.close()

    def start(self):
        multi_thread_chain(tuple((
            (task, {}) for task in self.tasks
        )))
