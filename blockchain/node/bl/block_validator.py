import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import Dict, List
from node.bl.transaction import Transaction
from node.bl.unified_block import UnifiedBlock
from node.bl.exceptions import BlockValidationException
from node.dal.blockchain_db.blockchain_data_manager_sql import BlockchainDataManager
from node.dal.utxo_db.utxo_data_manager_sql import UtxoDataManager
from node.dal.utils.exceptions import BlockchainDatabaseException, UtxoDatabaseException
from datetime import datetime, timedelta

TIMESTAMP_DELTA_VALIDATION = 30  # 30 Minutes possible offset to the future

class BlockValidator:

    # def __init__(self, unified_block: UnifiedBlock):
    #     self.unified_block = unified_block

    # @property
    # def unified_block(self) -> UnifiedBlock:
    #     return self._unified_block

    # @unified_block.setter
    # def unified_block(self, new_unified_block: UnifiedBlock) -> None:
    #     self._unified_block = new_unified_block

    def validate_block():
        # validate hash (smaller than difficulty defined by the node, contain all items)
        # validate first tx (coinbase) --DONE--
        # validate all txs are UTXO
        # validate all txs relate to this block --DONE--
        # validate height + prev_block_hash --DONE--
        # validate merkle root (simple hash of all tx's, no tree) --DONE--
        # timestamp: 30 min advance --DONE--
        pass


    @staticmethod
    def __validate_first_tx(tx_list: List[Transaction]) -> bool:
        if len(tx_list) == 0 or tx_list is None:
            raise BlockValidationException("No tx's exist in the block. At least coinbase tx should exist")
        
        first_tx = list(filter(lambda tx: tx.tx_block_index == 1, tx_list))[0]
        if len(first_tx.vin) != 1:
            raise BlockValidationException("First tx doesn't have specifically 1 vin")

        if first_tx.vin[0]['vin_addr'] != "coinbase":
            raise BlockValidationException("First tx must be a coinbase tx")

        return True
        #TODO: implement coinbase amount verification

    @staticmethod
    def __validate_txs_related_to_block(unified_b: UnifiedBlock) -> bool:
        txs_blocks = list(map(lambda tx: tx.tx_block_hash, unified_b.tx_list))
        if len(list(filter(lambda tx_block: tx_block != unified_b.hash, txs_blocks))) > 0:
            raise BlockValidationException("Not all tx's in block are related to the required block")

        return True


    @staticmethod
    def __validate_merkle_root(unified_b: UnifiedBlock) -> bool:
        if UnifiedBlock.calc_block_merkle_root(block=unified_b) != unified_b.merkle_root:
            raise BlockValidationException("Merkle root of the block does not fit the txs exist in it")

        return True


    @staticmethod
    def __validate_block_timestamp(unified_b: UnifiedBlock) -> bool:
        current_timestamp_with_delta = datetime.timestamp(
            datetime.now() + timedelta(minutes=TIMESTAMP_DELTA_VALIDATION)
        )
        if unified_b.timestamp > current_timestamp_with_delta:
            raise BlockValidationException("Block timestamp is too far away in the future")

        return True


    @staticmethod
    def __validate_prev_block_hash(unified_b: UnifiedBlock) -> bool:
        bc_data_manager = BlockchainDataManager()
        try:
            latest_block: Dict = bc_data_manager.get_latest_block()
        except BlockchainDatabaseException:
            raise BlockValidationException("Could not verify the prev_block_hash since it doesn't exist in the blockchain.")

        # prev_block_hash of the new block needs to be as the hash of the latest existing block in the node
        if unified_b.prev_block_hash != latest_block['hash']:
            raise BlockValidationException("Hash of latest blockchain block does not fit the prev_block_hash in the new block.")

        return True


    @staticmethod
    def __validate_block_height(unified_b: UnifiedBlock) -> bool:
        bc_data_manager = BlockchainDataManager()
        try:
            latest_block: Dict = bc_data_manager.get_latest_block
        except BlockchainDatabaseException:
            raise BlockValidationException("Could not verify the height since no more blocks exists in the blockchain")
        
        # new block's height should be heigher by 1 than the latest block
        if unified_b.height != latest_block['height'] + 1:
            raise BlockValidationException(f"Height of the new block is incorrect, and should be {latest_block['height'] + 1}")

        return True


    @staticmethod
    def validate_all_txs_are_utxo(unified_b: UnifiedBlock) -> bool:
        utxo_data_manager = UtxoDataManager()
        for tx in unified_b.tx_list:
            try:
                utxo_data_manager.get_utxo_by_txid(tx.txid)
            # Needed a hotfix here. BlockException is not raising
            except UtxoDatabaseException:
                raise BlockValidationException("Some txs in the block are not UTXO's.")

        return True



vin_tx1 = [{
        "vin_addr": "coinbase",
        "vin_value": 6000,
        "vin_script": "a0a0a0a0a0a0a0a0a0"
    }]

tx_1 = Transaction(tx_block_hash="00000000000000027e7ba6fe7bad39faf3b5a83daed765f05f7d1b71a1632249",
                        tx_block_index=1,
                        vin=vin_tx1,
                        vout_addr="1Bpqjnfrp4BKxdGFKs1akUzzqxAEW6dVBU",
                        vout_value=6000,
                        vout_script="76bd7e03396843873ceda9815b392e5bab45b330",
                        vchange_addr="1Bpqjnfrp4BKxdGFKs1akUzzqxAEW6dVBU",
                        vchange_value=0,
                        vchange_script="04a39b9e4fbd213ef24bb9be69de4a118dd0644082e47c01fd9159d38637b83f" + \
                        "bcdc115a5d6e970586a012d1cfe3e3a8b1a3d04e763bdc5a071c0e827c0bd834a5")
tx_1.txid = '12423'

vin_tx2 = [{
        "vin_addr": "1VayNert3x1KzbpzMGt2qdqrAThiRov55",
        "vin_value": 627907074,
        "vin_script": "3046022100cf19e206eb882624d9631a443eaf4925894" + \
            "3040e9c680bf054881e548606ee77022100a1d624adf36015bfb772171046b" + \
            "1aa2edbed7c1fd20ec8c57fabaaebf031266666"
    },
    {
        "vin_addr": "1VayNert3x1KzbpzMGt2qdqrAThiRov55",
        "vin_value": 120000000,
        "vin_script": "3046022100cf19e206eb882624d9631a443eaf4925894" + \
            "3040e9c680bf054881e548606ee77022100a1d624adf36015bfb772171046b" + \
            "1aa2edbed7c1fd20ec8c57fabaaebf03555"
    }]

tx_2 = Transaction(tx_block_hash="00000000000000027e7ba6fe7bad39faf3b5a83daed765f05f7d1b71a1632249",
                        tx_block_index=2,
                        vin=vin_tx2,
                        vout_addr="1Bpqjnfrp4BKxdGFKs1akUzzqxAEW6dVBU",
                        vout_value=90000000,
                        vout_script="76bd7e03396843873ceda9815b392e5bab45b330",
                        vchange_addr="1VayNert3x1KzbpzMGt2qdqrAThiRovi8",
                        vchange_value=537907074,
                        vchange_script="04a39b9e4fbd213ef24bb9be69de4a118dd0644082e47c01fd9159d38637b83f" + \
                        "bcdc115a5d6e970586a012d1cfe3e3a8b1a3d04e763bdc5a071c0e827c0bd834a5")
tx_2.txid = '98798789'

unified_b = UnifiedBlock(hash="00000000000000027e7ba6fe7bad39faf3b5a83daed765f05f7d1b71a1632249",
                    prev_block_hash="00000000000000027e7ba6fe7bad39faf3b5a83daed765f05f7d173951632249",
                    merkle_root="5e049f4030e0ab2debb92378f53c0a6e09548aea083f3ab25e1d94ea1155e29d",
                    timestamp=datetime.timestamp(
                        datetime.now()),
                    difficulty=180923195.25802612,
                    nonce=4215469401,
                    height=124193,
                    tx_list=[tx_1, tx_2])

bv = BlockValidator()
bv.validate_all_txs_are_utxo(unified_b=unified_b)
