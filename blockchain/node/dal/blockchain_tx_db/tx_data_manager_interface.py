from re import sub
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import abc
from typing import Dict
from bl.transaction import Transaction

class NodeTransactionInterface(abc.ABC):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_tx_by_hash') and
        callable(subclass.get_tx_by_hash) and
        hasattr(subclass, 'get_tx_by_block_hash') and
        callable(subclass.get_tx_by_block_hash) and
        hasattr(subclass, 'set_new_tx') and
        callable(subclass.set_new_tx) and
        hasattr(subclass, 'update_tx_by_hash') and
        callable(subclass.update_tx_by_hash) and
        hasattr(subclass, 'delete_tx_by_hash') and
        callable(subclass.delete_tx_by_hash) or
        NotImplemented)

    @abc.abstractclassmethod
    def get_tx_by_hash(self, hash: str) -> Dict:
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_tx_by_block_hash(self, block_hash: str) -> Dict:
        raise NotImplementedError

    @abc.abstractclassmethod
    def set_new_tx(self, tx: Transaction) -> None:
        raise NotImplementedError

    @abc.abstractclassmethod
    def update_tx_by_hash(self, hash: str, tx: Transaction) -> None:
        raise NotImplementedError

    @abc.abstractclassmethod
    def delete_tx_by_hash(self, hash: str) -> None:
        raise NotImplementedError
