import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import Dict, List
from node.dal.utils.exceptions import TxPoolDatabaseException
from node.dal.tx_pool_db.tx_pool_data_manager_sql import TxPoolDataManager
from node.bl.transaction import Transaction
from node.bl.unified_block import UnifiedBlock
from node.bl.exceptions import BlockValidationException
from node.dal.blockchain_db.blockchain_data_manager_sql import BlockchainDataManager
from node.dal.utxo_db.utxo_data_manager_sql import UtxoDataManager
from node.dal.utils.exceptions import BlockchainDatabaseException
from datetime import datetime, timedelta

TIMESTAMP_DELTA_VALIDATION = 30  # 30 Minutes possible offset to the future
COINBASE_ADDR = "coinbase"
DIFFICULTY_BITS = 256 # as of the hash size (sha-256)

class BlockValidator:

    def validate_block(self, unified_block: UnifiedBlock, req_difficulty: float) -> bool:
        """
        validate hash (smaller than difficulty defined by the node, contain all items)
        validate first tx (coinbase)
        validate all txs are UTXO
        validate all txs relate to this block
        validate height + prev_block_hash
        validate merkle root (simple hash of all tx's, no tree)
        timestamp: 30 min advance
        """
        return BlockValidator.__validate_first_tx(tx_list=unified_block.tx_list) and BlockValidator.__validate_txs_related_to_block(unified_b=unified_block) \
            and BlockValidator.__validate_merkle_root(unified_b=unified_block) and BlockValidator.__validate_block_timestamp(unified_b=unified_block) \
            and BlockValidator.__validate_prev_block_hash(unified_b=unified_block) and BlockValidator.__validate_block_height(unified_b=unified_block) \
            and BlockValidator.__validate_all_txs_are_from_pool(unified_b=unified_block) and BlockValidator.__validate_block_difficulty(unified_block, req_difficulty) \
            and BlockValidator.__validate_block_hash(unified_b=unified_block, req_difficulty=req_difficulty)


    @staticmethod
    def __validate_first_tx(tx_list: List[Transaction]) -> bool:
        if len(tx_list) == 0 or tx_list is None:
            raise BlockValidationException("No tx's exist in the block. At least coinbase tx should exist")
        
        if len(tx_list) == 1 and tx_list[0].tx_block_index != 1:
            raise BlockValidationException("The only tx exists is not a coinbase transaction")

        first_tx = list(filter(lambda tx: tx.tx_block_index == 1, tx_list))[0]
        if len(first_tx.vin) != 1:
            raise BlockValidationException("First tx doesn't have specifically 1 vin")

        if first_tx.vin[0]['vin_addr'] != COINBASE_ADDR:
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
            latest_block: Dict = bc_data_manager.get_latest_block()
        except BlockchainDatabaseException:
            raise BlockValidationException("Could not verify the height since no more blocks exists in the blockchain")
        
        # new block's height should be heigher by 1 than the latest block
        if unified_b.height != latest_block['height'] + 1:
            raise BlockValidationException(f"Height of the new block is incorrect, and should be {latest_block['height'] + 1}")

        return True


    @staticmethod
    def __validate_all_txs_are_from_pool(unified_b: UnifiedBlock) -> bool:
        tx_pool_data_manager = TxPoolDataManager()
        utxo_data_manager = UtxoDataManager()

        tx_list_without_coinbase_tx = list(filter(lambda tx: tx.tx_block_index != 1, unified_b.tx_list))

        for tx in tx_list_without_coinbase_tx: # Check all tx's but coinbase
            try:
                tx_pool_data_manager.get_tx_by_txid(txid=tx.txid)
            except TxPoolDatabaseException:
                raise BlockValidationException("Some txs in the block are not UTXO's.")

        return True

    @staticmethod
    def __validate_block_difficulty(unified_b: UnifiedBlock, req_difficulty: float) -> bool:
        if unified_b.difficulty < req_difficulty:
            raise BlockValidationException("Block's difficulty isn't enough")

        return True


    @staticmethod 
    def __validate_block_hash(unified_b: UnifiedBlock, req_difficulty: float) -> bool:
        """ Node validates 2 things:
        1. Block hash is in the correct format
        2. Block hash is smaller than the required difficulty
        """
        
        excpected_hash = unified_b.calc_block_hash()

        if unified_b.hash != excpected_hash:
            raise BlockValidationException("Block hash does not meet the hashing standard")

        if not BlockValidator.__validate_block_hash_val_by_difficulty(unified_b=unified_b, 
                                                                      req_difficulty=req_difficulty):
            raise BlockValidationException("Block does not stand the required difficulty")

        return True


    @staticmethod
    def __validate_block_hash_val_by_difficulty(unified_b: UnifiedBlock, req_difficulty: float) -> bool:
        return False if int(unified_b.hash, 16) > (2 ** (DIFFICULTY_BITS - req_difficulty)) else True

