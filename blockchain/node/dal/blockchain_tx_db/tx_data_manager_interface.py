import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import abc
from typing import Dict, List
from bl.transaction import Transaction

class NodeTransactionInterface(abc.ABC):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_tx_by_txid') and
        callable(subclass.get_tx_by_txid) and
        hasattr(subclass, 'get_txs_by_block_hash') and
        callable(subclass.get_txs_by_block_hash) and
        hasattr(subclass, 'set_new_tx') and
        callable(subclass.set_new_tx) and
        hasattr(subclass, 'update_tx_by_txid') and
        callable(subclass.update_tx_by_txid) and
        hasattr(subclass, 'delete_tx_by_txid') and
        callable(subclass.delete_tx_by_txid) or
        NotImplemented)

    @abc.abstractclassmethod
    def get_tx_by_txid(self, txid: str) -> Dict:
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_txs_by_block_hash(self, block_hash: str) -> List[Dict]:
        raise NotImplementedError

    @abc.abstractclassmethod
    def set_new_tx(self, tx: Transaction) -> None:
        raise NotImplementedError

    @abc.abstractclassmethod
    def update_tx_by_txid(self, txid: str, tx: Transaction) -> None:
        raise NotImplementedError

    @abc.abstractclassmethod
    def delete_tx_by_txid(self, txid: str) -> None:
        raise NotImplementedError
