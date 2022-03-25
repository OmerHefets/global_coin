import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from node.bl.node_managers.blockchain_manager import BlockchainManager
from node.bl.node_managers.tx_manager import TxManager
from node.bl.node_managers.tx_pool_manager import TxPoolManager
from node.bl.node_managers.utxo_manager import UtxoManager


class BazookaClient:

    def __init__(self) -> None:
        self.blockchain_manager = BlockchainManager()
        self.tx_manager = TxManager()
        self.tx_pool_manager = TxPoolManager()
        self.utxo_manager = UtxoManager()
