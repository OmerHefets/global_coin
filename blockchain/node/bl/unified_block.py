import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from node.bl.transaction import Transaction
from node.bl.block import Block
from typing import List, Dict
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


    def __repr__(self) -> str:
        return f"""UnifiedBlock(hash='{self.hash}',
        prev_block_hash='{self.prev_block_hash}',
        merkle_root='{self.merkle_root}',
        timestamp={self.timestamp},
        difficulty={self.difficulty},
        nonce={self.nonce},
        height={self.height},
        tx_list={self.tx_list}"""


    @property
    def tx_list(self) -> List[Transaction]:
        return self._tx_list


    @tx_list.setter
    def tx_list(self, new_tx_list) -> None:
        self._tx_list = new_tx_list


    def add_tx(self, tx: Transaction) -> None:
        self.tx_list = self.tx_list + [tx] # No change to tx_list in place


    @staticmethod
    def init_unified_block_from_dict(unified_block_dict: Dict):
        return UnifiedBlock(hash=unified_block_dict['hash'],
                          prev_block_hash=unified_block_dict['prev_block_hash'],
                          merkle_root=unified_block_dict['merkle_root'],
                          timestamp=unified_block_dict['timestamp'],
                          difficulty=unified_block_dict['difficulty'],
                          nonce=unified_block_dict['nonce'],
                          height=unified_block_dict['height'],
                          tx_list=[Transaction.init_tx_from_dict(tx_dict) for tx_dict in unified_block_dict['tx_list']]) 


    @staticmethod
    def convert_unified_block_to_dict(unified_block) -> Dict:
        return {
            'hash': unified_block.hash,
            'prev_block_hash': unified_block.prev_block_hash,
            'merkle_root': unified_block.merkle_root,
            'timestamp': unified_block.timestamp,
            'difficulty': unified_block.difficulty,
            'nonce': unified_block.nonce,
            'height': unified_block.height,
            'tx_list': [Transaction.convert_tx_to_dict(tx) for tx in unified_block.tx_list]
        }


    @staticmethod
    def calc_block_merkle_root(block):
        tx_list_ordered = sorted(block.tx_list, key=lambda tx: tx.tx_block_index, reverse=False)

        # hash tx's by order (Not a regular merkle root calc)
        merkle_root_hash_str = str.encode(reduce(lambda x, y: x+y, \
        list(map(lambda tx: tx.txid, tx_list_ordered))))

        sha256_hash = sha256()
        sha256_hash.update(merkle_root_hash_str)

        return sha256_hash.hexdigest()


    def calc_block_hash(self):
        # in this implementation, block hash is calculated based on:
        # timestamp + prev_block_hash + merkle_root + nonce
        block_string = (str(self.timestamp) + self.prev_block_hash + self.merkle_root \
            + str(self.nonce)).encode()

        sha256_hash = sha256()
        sha256_hash.update(block_string)

        return sha256_hash.hexdigest()