import abc
from typing import Dict
from block import Block


class NodeBlockchainInterface(abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return True

    @abc.abstractmethod
    def get_block_by_hash(hash: str) -> Dict:
        raise NotImplementedError

    @abc.abstractmethod
    def get_block_by_height(height: int) -> Dict:
        raise NotImplementedError

    @abc.abstractmethod
    def add_new_block(block: Block) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def update_block(block: Block) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_block(block: Block) -> None:
        raise NotImplementedError
