import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import Dict, List
from node.bl.unified_block import UnifiedBlock
from exceptions import BlockValidationException


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
        # validate all txs relate to this block
        # validate height + prev_block_hash
        # validate merkle root (simple hash of all tx's, no tree)
        # timestamp: 30 min advance / lag
        pass


    @staticmethod
    # change this to by tx_block_index...
    def validate_first_tx(vin: List[Dict]) -> bool:
        if len(vin) == 0 or vin is None:
            raise BlockValidationException("No tx's exist in the block. At least coinbase tx should exist")
        
        first_tx = vin[0]
        if first_tx['vin_addr'] != "coinbase":
            raise BlockValidationException("First tx must be a coinbase tx")

        return True
        #TODO: implement coinbase amount verification


