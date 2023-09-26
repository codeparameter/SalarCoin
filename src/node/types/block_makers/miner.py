from src.node.types.node import Node


class Miner(Node):

    def __init__(self, ip, sk):
        super().__init__(ip, sk)
        self.tasks += [
            self.mine,
        ]

    # factory and seed management:

    @staticmethod
    def downcast_cls_method(cls_method, *args, **kwargs):
        return Node.downcast_cls_method(Miner, cls_method, *args, **kwargs)

    @staticmethod
    def downcast_static_method(static_method, *args, **kwargs):
        return Node.downcast_static_method(Miner, static_method, *args, **kwargs)

    # mine management:

    def mine(self):
        # TODO
        pass

    # CLI management:

    @staticmethod
    def run():
        pass
