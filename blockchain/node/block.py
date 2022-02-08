from typing import Dict
from datetime import datetime, timedelta
from exceptions import BlockException

HASH_LENGTH = 64  # hash is 32 bytes from SHA-256 hash function
TIMESTAMP_DELTA_VALIDATION = 1  # 1 minute delay in a block processing


class Block:
    def __init__(self,
                 hash: str,
                 prev_block_hash: str,
                 merkle_root: str,
                 timestamp: datetime,
                 difficulty: float,
                 nonce: int,
                 height: int) -> None:
        self.hash = hash
        self.prev_block_hash = prev_block_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.difficulty = difficulty
        self.nonce = nonce
        self.height = height

    def __repr__(self) -> str:
        return f"""Block(hash={self.hash},
        prev_block_hash={self.prev_block_hash},
        merkle_root={self.merkle_root},
        timestamp={self.timestamp},
        difficulty={self.difficulty},
        nonce={self.nonce},
        height={self.height})
        """

    @property
    def hash(self) -> str:
        return self._hash

    @hash.setter
    def hash(self, new_hash) -> None:
        if not self.hash_validation(new_hash):
            raise BlockException("Invalid hash value")
        self._hash = new_hash

    @property
    def prev_block_hash(self) -> str:
        return self._prev_block_hash

    @prev_block_hash.setter
    def prev_block_hash(self, new_hash) -> None:
        if not self.hash_validation(new_hash):
            raise BlockException("Invalid prev hash value")
        self._prev_block_hash = new_hash

    @property
    def merkle_root(self) -> str:
        return self._merkle_root

    @merkle_root.setter
    def merkle_root(self, new_root) -> None:
        self._merkle_root = new_root

    @property
    def timestamp(self) -> float:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, new_timestamp) -> None:
        if not self.timestamp_validation(new_timestamp):
            raise BlockException("Invalid timestamp value")
        self._timestamp = new_timestamp

    @property
    def difficulty(self) -> float:
        return self._difficulty

    @difficulty.setter
    def difficulty(self, new_difficulty) -> None:
        if not self.difficulty_validation(new_difficulty):
            raise BlockException("Invalid difficulty value")
        self._difficulty = new_difficulty

    @property
    def nonce(self) -> int:
        return self._nonce

    @nonce.setter
    def nonce(self, new_nonce) -> None:
        if not self.nonce_validation(new_nonce):
            raise BlockException("Invalid nonce value")
        self._nonce = new_nonce

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, new_height) -> None:
        if not self.height_validation(new_height):
            raise BlockException("Invalid height value")
        self._height = new_height

    @staticmethod
    def hash_validation(hash) -> bool:
        if not isinstance(hash, str) or len(hash) < HASH_LENGTH:
            return False
        else:
            return True

    @staticmethod
    def timestamp_validation(timestamp) -> bool:
        current_timestamp_with_delta = datetime.timestamp(
            datetime.now() + timedelta(minutes=TIMESTAMP_DELTA_VALIDATION))
        if not isinstance(timestamp, float) or timestamp > current_timestamp_with_delta:
            return False
        else:
            return True

    @staticmethod
    def nonce_validation(nonce) -> bool:
        return False if not isinstance(nonce, int) else True

    @staticmethod
    def difficulty_validation(difficulty) -> bool:
        return False if not isinstance(difficulty, float) else True

    @staticmethod
    def height_validation(height) -> bool:
        return False if not isinstance(height, int) else True

    def convert_block_to_dict(self) -> Dict:
        block_dict = {
            "hash": self.hash,
            "prev_block_hash": self.prev_block_hash,
            "merkle_root": self.merkle_root,
            "timestamp": self.timestamp,
            "difficulty": self.difficulty,
            "nonce": self.nonce,
            "height": self.height
        }
        return block_dict
