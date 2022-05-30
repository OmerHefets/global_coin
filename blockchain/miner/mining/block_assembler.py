import sys
sys.path.append("")

from string import ascii_lowercase
import random
from requests import get
from typing import Dict, List
from node.bl.unified_block import UnifiedBlock
from node.bl.transaction import Transaction
from datetime import datetime

LATEST_BLOCK_ROUTE = "/blockchain/latest"
TOP_100_TXS = "/tx_pool/top_100"
RAND_SCRIPT_LEN = 30

class BlockAssembler:

    def __init__(self, miner_addr: str, node_url: str, difficulty: int) -> None:
        self.miner_addr = miner_addr
        self.node_url = node_url
        self.difficulty = difficulty


    def get_prev_block_info(self):
        latest_block: Dict = get(url=(self.node_url+LATEST_BLOCK_ROUTE)).json()
        return (latest_block['hash'], latest_block['height'])

    
    def create_tx_list(self) -> List:
        return [self.__create_coinbase_tx()] + self.__get_tx_list_from_tx_pool()


    def __get_tx_list_from_tx_pool(self) -> List[Transaction]:
        top_100_txs_from_pool: List[Dict] = get(url=(self.node_url+TOP_100_TXS)).json()
        top_100_txs_from_pool: List[Transaction] = [Transaction.init_tx_from_dict(tx_dict) for tx_dict in top_100_txs_from_pool]
        return top_100_txs_from_pool 


    def __create_coinbase_tx(self) -> Transaction:
        return Transaction(tx_block_hash="-1",
                           tx_block_index=1,
                           vin=[{
                               'txid': "0",
                               'vin_addr': "coinbase",
                               'vin_value': 50,
                               'vin_script': ''.join(random.choice(ascii_lowercase) for i in range(RAND_SCRIPT_LEN))
                           }],
                           vout_addr=self.miner_addr,
                           vout_value=50,
                           vchange_addr=self.miner_addr,
                           vchange_value=0)


    def assemble_pre_hash_unified_block(self) -> UnifiedBlock:
        prev_block_hash, prev_height = self.get_prev_block_info()
        return UnifiedBlock(hash=('0' * 64),
                            prev_block_hash=prev_block_hash,
                            merkle_root="42",
                            timestamp=datetime.timestamp(datetime.now()),
                            difficulty=self.difficulty,
                            nonce=1,
                            height=(prev_height + 1),
                            tx_list=self.create_tx_list())


    def update_unified_block_txs_hash(self, unified_block: UnifiedBlock) -> UnifiedBlock:
        temp_unified_block = unified_block

        for tx in temp_unified_block.tx_list:
            tx.tx_block_hash = temp_unified_block.hash
