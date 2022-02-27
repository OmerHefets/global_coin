import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

HASH_LENGTH = 64  # hash is 32 bytes from SHA-256 hash function

class Transaction:
    def __init__(self,
                 id, 
                 block_hash) -> None:
        self.id = id
        self.block_hash = block_hash

    def __repr__(self) -> str:
        return f"""Transaction(id={self.id},
        block_hash={self.block_hash})"""

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, new_id) -> None:
        self._id = new_id

    @property
    def block_hash(self) -> str:
        return self._block_hash

    @block_hash.setter
    def block_hash(self, new_block_hash) -> None:
        self._block_hash = new_block_hash

