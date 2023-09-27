import hashlib
import sys

from dependencies.tools import dict_to_bytes
from .base_tx import BaseTx


class Meta(BaseTx):

    def __init__(self, vin_size, vout_size, lock_time=0, ver=1):  # TODo : lock time
        self.metadata = {
            'ver': ver,
            'vin_size': vin_size,
            'vout_size': vout_size,
        }
        self.hash = b''
        self.body = {}
        self.body_bytes = b''
        self.size = 0

    def set(self, inps, outs):
        self.body = {'in': inps, 'out': outs}
        self.body_bytes = dict_to_bytes(self.body)
        self.hash = hashlib.sha3_256(self.body_bytes)
        self.size = sys.getsizeof(self.body_bytes)
