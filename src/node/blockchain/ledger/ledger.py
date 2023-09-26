from .block.block import Block
from .block.tx.tx import Tx


class Ledger:

    def __init__(self, block_header: Block, sk, vk):
        self.header = block_header
        self.utxo: {str: Tx | Block} = {}  # also known as memory pool
        # str key in utxo is the hash pointer of a transaction
        self.sk = sk
        self.vk = vk

    def withdraw(self, unspent: list, outs):
        pass
