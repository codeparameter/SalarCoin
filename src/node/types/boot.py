from src.node.wallet import Hub, NODES_PER_SERVER
from src.node.base import Base

BOOTS = [
    Hub('98.231.89.198'),
    Hub('111.117.117.253'),
    Hub('25.45.205.230'),
    Hub('212.42.34.58'),
    Hub('46.235.1.8'),
    Hub('202.32.39.85'),
    Hub('200.203.24.240'),
    Hub('214.23.173.251'),
    Hub('65.254.234.234'),
    Hub('205.77.21.142'),
]


class Boot(Base):

    def __init__(self, ip, sk):
        super().__init__(ip, sk)

    # factory and seed management:

    @staticmethod
    def downcast_cls_method(cls_method, *args, **kwargs) -> 'Boot':
        return Base.downcast_cls_method(Boot, cls_method, *args, **kwargs)

    @staticmethod
    def downcast_static_method(static_method, *args, **kwargs):
        return Base.downcast_static_method(Boot, static_method, *args, **kwargs)

    # register management:

    # Hub.get_requests ->
    # noinspection PyBroadException
    def register_node(self, data):
        try:
            (verified, data, vk), (ip, port) = data
            if not verified:
                return None
            node = Hub.from_dict({'ip': ip, 'port': port}.update(data))
            start = data['start']
            neighbors = self.neighbors_list[start:start + NODES_PER_SERVER]
            self.add_neighbor(node)
            return self.sign_query(
                neighbors=neighbors
            )
        except Exception:
            return b'your data was corrupted'

    # static bootstrap node:

    @staticmethod
    def get_bootstrap_nodes():
        bootstrap_node_secret_keys = [
            '6451fb3a07b6075c0ca4270c57a1f038430f85a6de890748a4709394fce045c4',
            '9a9a7e6995ba0d90cc8e97f2198c683d22fd6b5bc28866595c984b2e88b20257',
            'f015301bf5c49e77edac730ca6754c45b21401c9cd4a33e2732b3a860fa4497f',
            'fac4d5e29011f72e97348a7e5a0a483d2b4231633e5b84a086a2c016c4f8eb20',
            '97ceb464b7266263c5d153b749ffb887cf939531acc42d0c68edc531a5b88e01',
            'cf5850162c8d27c8348a2a67829cda698e3cc922e0ef7b80ef37fc2fe505d9e9',
            '7ad51e0fd119410321b61097f023d6ea8542691e0d76eab2272e17f9db68d5fd',
            '78ec03edbe538a3c3048779cdebd5933e0062d557a5339343261b2b92fa5afbc',
            '3c02a21591bd46a348a116ec60a660f0179e2cdae8c731596edc87600b1c0a80',
            'b8ce90b250560482fd21371aa3732ed71fcd08bfa050a6319e1bc288ff48f511'
        ]
        return [Boot(bn.ip, bnk) for bn, bnk in
                zip(BOOTS, bootstrap_node_secret_keys)]

    # CLI management:

    @staticmethod
    def run():
        pass
