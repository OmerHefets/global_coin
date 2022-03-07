import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import Dict, List
from blockchain.node.bl.transaction import Transaction
from node.bl.unified_block import UnifiedBlock
from node.bl.exceptions import BlockValidationException
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
        # validate height + prev_block_hash
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


