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
        self.merkle_root = self.calc_block_merkle_root()

    @property
    def tx_list(self) -> List[Transaction]:
        return self._tx_list

    @tx_list.setter
    def tx_list(self, new_tx_list) -> None:
        self._tx_list = new_tx_list

    def add_tx(self, tx: Transaction) -> None:
        self.tx_list = self.tx_list + [tx] # No change to tx_list in place

    def calc_block_merkle_root(self):
        tx_list_ordered = sorted(self.tx_list, key=lambda tx: tx.tx_block_index, reverse=False)

        # hash tx's by order (Not a regular merkle root calc)
        merkle_root_hash_str = str.encode(reduce(lambda x, y: x+y, \
        list(map(lambda tx: tx.txid, tx_list_ordered))))

        sha256_hash = sha256()
        sha256_hash.update(merkle_root_hash_str)

        return sha256_hash.hexdigest()



# vin_adv = [{
#         "vin_addr": "1VayNert3x1KzbpzMGt2qdqrAThiRov55",
#         "vin_value": 627907074,
#         "vin_script": "3046022100cf19e206eb882624d9631a443eaf4925894" + \
#             "3040e9c680bf054881e548606ee77022100a1d624adf36015bfb772171046b" + \
#             "1aa2edbed7c1fd20ec8c57fabaaebf031266666"
#     },
#     {
#         "vin_addr": "1VayNert3x1KzbpzMGt2qdqrAThiRov55",
#         "vin_value": 120000000,
#         "vin_script": "3046022100cf19e206eb882624d9631a443eaf4925894" + \
#             "3040e9c680bf054881e548606ee77022100a1d624adf36015bfb772171046b" + \
#             "1aa2edbed7c1fd20ec8c57fabaaebf03555"
#     }]

# t = Transaction(tx_block_hash="00000000000009dff396a335faf0c7a834b5543bd63267bb4d7ecf53fb36377e",
#                        tx_block_index=4,
#                        vin=vin_adv,
#                        vout_addr="1Bpqjnfrp4BKxdGFKs1akUzzqxAEW6dVBU",
#                        vout_value=90000000,
#                        vout_script="76bd7e03396843873ceda9815b392e5bab45b330",
#                        vchange_addr="1VayNert3x1KzbpzMGt2qdqrAThiRovi8",
#                        vchange_value=537907074,
#                        vchange_script="04a39b9e4fbd213ef24bb9be69de4a118dd0644082e47c01fd9159d38637b83f" + \
#                        "bcdc115a5d6e970586a012d1cfe3e3a8b1a3d04e763bdc5a071c0e827c0bd834a5")


# ub = UnifiedBlock(hash="00000000000000027e7ba6fe7bad39faf3b5a83daed765f05f7d1b71a1632249",
#                  prev_block_hash="00000000000000027e7ba6fe7bad39faf3b5a83daed765f05f7d173951632249",
#                  merkle_root="5e049f4030e0ab2debb92378f53c0a6e09548aea083f3ab25e1d94ea1155e29d",
#                  timestamp=datetime.timestamp(
#                      datetime.now()),
#                  difficulty=180923195.25802612,
#                  nonce=4215469401,
#                  height=124193,
#                  tx_list=[t])

# print(ub._tx_list)