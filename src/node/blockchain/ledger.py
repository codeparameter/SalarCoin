from src.node.blockchain.ledger.block import Block
from src.node.wallet.keyobject import KeyObject


class Ledger:

    def __init__(self, block_header: Block, sk: KeyObject, vk: KeyObject):
        self.header = block_header
        self.utxo = {}  #
        self.sk = sk
        self.vk = vk

    def withdraw(self, unspent: list, outs):
        pass
