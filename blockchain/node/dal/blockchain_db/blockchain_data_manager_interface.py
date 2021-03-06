import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import abc
from typing import Dict
from bl.block import Block


class NodeBlockchainInterface(abc.ABC):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_latest_block') and
                callable(subclass.get_latest_block) and
                hasattr(subclass, 'get_block_by_hash') and
                callable(subclass.get_block_by_hash) and
                hasattr(subclass, 'get_block_by_height') and
                callable(subclass.get_block_by_height) and
                hasattr(subclass, 'add_new_block') and
                callable(subclass.add_new_block) and
                hasattr(subclass, 'update_block_by_hash') and
                callable(subclass.update_block_by_hash) and
                hasattr(subclass, 'delete_block_by_hash') and
                callable(subclass.delete_block_by_hash) or
                NotImplemented)

    @abc.abstractclassmethod
    def get_latest_block(self) -> Dict:
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_block_by_hash(self, hash: str) -> Dict:
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_block_by_height(self, height: int) -> Dict:
        raise NotImplementedError

    @abc.abstractclassmethod
    def add_new_block(self, block: Block) -> None:
        raise NotImplementedError

    @abc.abstractclassmethod
    def update_block_by_hash(self, hash: str, block: Block) -> None:
        raise NotImplementedError

    @abc.abstractclassmethod
    def delete_block_by_hash(self, hash: str) -> None:
        raise NotImplementedError
