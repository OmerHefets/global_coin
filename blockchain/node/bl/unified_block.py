import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from node.bl.transaction import Transaction
from node.bl.block import Block
from typing import List
from hashlib import sha256
from functools import reduce


class UnifiedBlock(Block):
    def __init__(self,
                 hash: str,
                 prev_block_hash: str,
                 merkle_root: str,
                 timestamp: float,
                 difficulty: float,
                 nonce: int,
                 height: int,
                 tx_list: List[Transaction]) -> None:
        super().__init__(hash=hash, prev_block_hash=prev_block_hash, merkle_root=merkle_root, timestamp=timestamp,
                         difficulty=difficulty, nonce=nonce, height=height)
        self.tx_list = tx_list
        self.merkle_root = self.calc_block_merkle_root(self)

    @property
    def tx_list(self) -> List[Transaction]:
        return self._tx_list

    @tx_list.setter
    def tx_list(self, new_tx_list) -> None:
        self._tx_list = new_tx_list

    def add_tx(self, tx: Transaction) -> None:
        self.tx_list = self.tx_list + [tx] # No change to tx_list in place

    @staticmethod
    def calc_block_merkle_root(block):
        tx_list_ordered = sorted(block.tx_list, key=lambda tx: tx.tx_block_index, reverse=False)

        # hash tx's by order (Not a regular merkle root calc)
        merkle_root_hash_str = str.encode(reduce(lambda x, y: x+y, \
        list(map(lambda tx: tx.txid, tx_list_ordered))))

        sha256_hash = sha256()
        sha256_hash.update(merkle_root_hash_str)

        return sha256_hash.hexdigest()

