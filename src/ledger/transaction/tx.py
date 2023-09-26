import json

from .metadata import Meta


class Tx(Meta):

    def __init__(self, inps, outs, vin_size, vout_size, lock_time, **_):
        super().__init__(vin_size, vout_size, lock_time)
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
        #   broadcast str(self) to connected nodes
        pass

    @classmethod
    def notice(cls, str_tx):
        # TODO
        return cls([], [], None)
