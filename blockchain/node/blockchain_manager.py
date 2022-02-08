import abc
from typing import Dict


class BlockchainManager(abc.ABCMeta):
    @abc.abstractmethod
    def get_block_by_hash(hash: str) -> Dict:
        raise NotImplementedError
