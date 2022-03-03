from node.bl.unified_block import UnifiedBlock

class BlockValidator:

    def __init__(self, unified_block: UnifiedBlock):
        self.unified_block = unified_block

    @property
    def unified_block(self) -> UnifiedBlock:
        return self._unified_block

    @unified_block.setter
    def unified_block(self, new_unified_block) -> None:
        self._unified_block = new_unified_block

    def validate_block():
        # validate hash (smaller than difficulty defined by the node, contain all items)
        # validate first tx (coinbase)
        # validate all txs are UTXO
        # validate all txs relate to this block
        # validate height + prev_block_hash
        # validate merkle root (simple hash of all tx's, no tree)
        # timestamp: 30 min advance / lag
        pass

