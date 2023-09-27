# mining reward & fee will go to miner account
# to spend rewards and fees, you can use the block hash as tx input
from .base_tx import BaseTx
from ..block import Block


class Inp:

    def __init__(self, Type: BaseTx | Block, ):
        pass
