import sys
sys.path.append("")

from blockchain.node.bl.unified_block import UnifiedBlock
from blockchain.node.bl.block_validator import DIFFICULTY_BITS


class Miner:

    def mine_block(self, unified_block: UnifiedBlock):
        unified_block.hash = unified_block.calc_block_hash()

        while int(unified_block.hash, 16) > (2 ** (DIFFICULTY_BITS - unified_block.difficulty)):
            unified_block.nonce += 1
            unified_block.hash = unified_block.calc_block_hash()

        return unified_block