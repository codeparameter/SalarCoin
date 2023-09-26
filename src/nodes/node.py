import random
import socket
from time import sleep

from dependencies.recursion import recursive, Continue
from dependencies.tools import multi_thread_chain, nxt
from src.helpers import log, asrt_not
from src.globals import SECONDS_PER_CRAWL
from .hub import Hub, NODES_PER_SERVER, CHOSEN_NODES, get_verified_query
from .base import Base
from .boot import BOOTS


class NodesNotFound(Exception):
    pass


class SomeNodesAreEmpty(Exception):
    pass


class NodesAreEmpty(Exception):
    pass


class CorruptedData(Exception):
    pass


# noinspection PyBroadException
class Node(Base):

    def __init__(self, ip, sk):
        super().__init__(ip, sk)
        self.tasks += [
            self.crawl,
            self.notice_tx,
            self.notice_block,
        ]
        self.boots = self.sort_list_by_dist(BOOTS)
        self.fine_nodes = []
        self.fine_boots = []

    # factory and seed management:

    @staticmethod
    def downcast_cls_method(cls_method, *args, **kwargs):
        return Base.downcast_cls_method(Node, cls_method, *args, **kwargs)

    @staticmethod
    def downcast_static_method(static_method, *args, **kwargs):
        return Base.downcast_static_method(Node, static_method, *args, **kwargs)

    # discovery and crawl management:

    def send_neighbors(self, data, ip, port):
        origin_node = Hub.from_dict({'ip': ip, 'port': port}.update(data))
        neighbors = self.neighbors_list[:NODES_PER_SERVER]
        self.add_neighbor(origin_node)
        return self.sign_query(
            neighbors=neighbors
        )

    #   Hub.send_request ->
    def update_neighbors(self, nodes: list):
        #  to add and sort neighbors after registration and every crawl response
        if len(nodes) == 0:
            return
        log('updating neighbors list...')
        nodes = self.from_dicts(nodes)
        self.add_neighbors(nodes)
        # data can be corrupted but it would handle eventually

    def send_request(self, nodes, fine, **query):
        target_node = nxt(nodes)
        if target_node is None:
            return None, SomeNodesAreEmpty

        query = self.sign_query(
            adr=self.adr.b58, **query
        )
        try:
            # server_address = (target_node.ip, target_node.port)  # commented for the sake of testing purposes
            server_address = ('127.0.0.1', target_node.port)
            # )
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(server_address)
            client_socket.sendall(query)
            # )
            response = client_socket.recv(1024)
            client_socket.close()
            fine.append(target_node)
            return get_verified_query(response), ''
        except Exception as err:
            return None, str(err)

    @recursive()
    def handle_res(self, res, err, nodes, fine, **query):
        if res:
            verified = res[0]
        else:
            verified = True
        if err != SomeNodesAreEmpty or not verified:
            res, err = self.send_request(nodes, fine, **query)
            return Continue(res, err, nodes, fine, **query)
        elif err:
            if not fine:
                return None, NodesAreEmpty
            nodes = iter(fine)
            res, err = self.send_request(nodes, fine, **query)
            return Continue(res, err, nodes, fine)
        else:
            return res, err

    def handle_corrupted_data(self,
                              res, err, nodes, fine,
                              res_fn, res_start=0, res_stop=3,
                              **query
                              ):
        if err:
            return err
        while True:
            try:
                res_fn(res[res_start:res_stop])
            except Exception:
                res, err = self.handle_res(None, CorruptedData, nodes, fine, **query)
                if res or err == NodesAreEmpty:
                    return err

    def request(self,
                nodes, fine,
                res_fn, res_start=0, res_stop=3,
                chosen_nodes=1,
                trying_log='',
                err_msg='',
                chained_fns=(), **query
                ):

        log(trying_log)
        err = NodesNotFound

        for i in range(chosen_nodes):
            res, err = self.send_request(nodes, fine, **query)
            res, err = self.handle_res(res, err, nodes, fine, **query)
            err = self.handle_corrupted_data(res, err, nodes, fine,
                                             res_fn,
                                             res_start=res_start,
                                             res_stop=res_stop,
                                             **query
                                             )

        asrt_not(err, err_msg, multi_thread_chain)(*chained_fns)

    def register(self):
        self.request(
            nodes=iter(self.boots),
            fine=self.fine_boots,
            chosen_nodes=CHOSEN_NODES,
            res_fn=self.update_neighbors,
            res_start=1,
            res_stop=2,
            trying_log='trying to register in network...',
            err_msg='registration was not successful',
            chained_fns=(
                (log, 'neighbors list updated\nyou successfully registered in network', {}),
                (self.start, {})
            ),
            # query:
            start=len(self.neighbors_list),
            route='node/register',
        )

    def crawl(self):
        while True:
            sleep(SECONDS_PER_CRAWL)
            node = random.choice(self.neighbors_list)
            self.request(
                res_fn=self.update_neighbors,
                res_start=1,
                res_stop=2,
                nodes=iter([node]),
                fine=self.fine_boots,
                trying_log='crawling into network...',
                err_msg='crawling was not successful',
                chained_fns=(
                    (log, 'neighbors list updated\nyou successfully crawled into network', {}),
                ),
                # query:
                route='node/crawl',
            )

    # tx and block management:

    def notice_tx(self):
        # TODO
        pass

    def propagate_tx(self):
        # TODO
        #  Thread
        pass

    def notice_block(self):
        # TODO
        pass

    def propagate_block(self):
        # TODO
        #  Thread
        pass

    # CLI management:

    @staticmethod
    def run():
        pass
