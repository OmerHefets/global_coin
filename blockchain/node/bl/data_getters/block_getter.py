import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import Tuple
from dal.blockchain_db.blockchain_data_manager_sql import BlockchainDataManager
from dal.utils.exceptions import BlockchainDatabaseException
from fastapi import status

class BlockGetter:
    def __init__(self) -> None:
        self.blockchain_db = BlockchainDataManager()


    def get_block_by_hash(self, hash: str) -> Tuple:
        try:
            block = self.blockchain_db.get_block_by_hash(hash=hash)
            return (status.HTTP_200_OK, block)
        except BlockchainDatabaseException:
            return (status.HTTP_404_NOT_FOUND, None)


    def get_block_by_height(self, height: int) -> Tuple:
        try:
            block = self.blockchain_db.get_block_by_height(height=height)
            return (status.HTTP_200_OK, block)
        except BlockchainDatabaseException:
            return (status.HTTP_404_NOT_FOUND, None)
