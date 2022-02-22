import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import Dict

from node.dal.node_blockchain_interface import NodeBlockchainInterface
from node.bl.block import Block


class BlockchainDataManager(NodeBlockchainInterface):
    

    def get_block_by_hash(self, hash: str) -> Dict:
        return {}

    def get_block_by_height(self, height: int) -> Dict:
        return {}

    def add_new_block(self, block: Block) -> None:
        pass

    def update_block(self, block: Block) -> None:
        pass

    def delete_block(self, block: Block) -> None:
        pass


a = BlockchainDataManager()