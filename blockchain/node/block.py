from datetime import datetime
from exceptions import BlockException

HASH_LENGTH = 64 # hash is 32 bytes

class Block:
    def __init__(self, hash: str,
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

    @property
    def hash(self):
        return self._hash

    @hash.setter
    def hash(self, new_hash):
        if not self.hash_validation(new_hash):
            raise BlockException("Invalid hash value.")
        self._hash = new_hash

    @staticmethod
    def hash_validation(hash) -> bool:
        if not isinstance(hash, str) or len(hash) < 2:
            return False
        else:
            return True
        

# b = Block("123", "234", "4323", datetime(year=2020, month=11, day=12), 1.23, 10, 1)
# print(b)
# if type(5) == int:
#    raise BlockException("WoW")
