import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import abc
from typing import Dict
from bl.transaction import Transaction

class NodeUtxoInterface(abc.ABC):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_utxo_by_txid') and
                callable(subclass.get_utxo_by_txid) and
                hasattr(subclass, 'get_utxos_by_addr') and
                callable(subclass.get_utxos_by_addr) and
                hasattr(subclass, 'add_new_utxo') and
                callable(subclass.add_new_utxo) and
                hasattr(subclass, 'update_utxo_by_txid') and
                callable(subclass.update_utxo_by_txid) and
                hasattr(subclass, 'delete_utxo_by_txid') and
                callable(subclass.delete_utxo_by_txid) or
                NotImplemented)

    @abc.abstractclassmethod
    def get_utxo_by_txid(self, txid: str) -> Dict:
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_utxos_by_addr(self, addr: str) -> Dict:
        raise NotImplementedError

    @abc.abstractclassmethod
    def add_new_utxo(self, utxo: Transaction) -> None:
        raise NotImplementedError

    @abc.abstractclassmethod
    def update_utxo_by_txid(self, txid: str, utxo: Transaction) -> None:
        raise NotImplementedError

    @abc.abstractclassmethod
    def delete_utxo_by_txid(self, txid: str) -> None:
        raise NotImplementedError

