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
        # validate hash
        # validate first tx (coinbase)
        # validate all txs are UTXO
        # validate all txs relate to this block
        pass

