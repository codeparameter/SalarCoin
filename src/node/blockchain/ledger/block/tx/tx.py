import json

from .meta import Meta
from .inp import Inp
from .out import Out


# mining reward & fee will go to miner account
# to spend rewards and fees, you can use the block hash as tx input

class Tx(Meta):

    def __init__(self, inps: [Inp], outs: [Out], vin_size, vout_size, **_):  # TODo : lock time
        super().__init__(vin_size, vout_size)
        self.set(inps, outs)

    @classmethod
    def init(cls, string):
        return cls(**string)

    def __str__(self):
        return json.dumps({
            'hash': self.hash,
            **self.metadata,
            'size': self.size,
            **self.body,
        })

    def notif(self, nodes):
        # TODO
        #   broadcast str(self) to connected node
        pass

    @classmethod
    def notice(cls, str_tx):
        # TODO
        return cls([], [], None)
