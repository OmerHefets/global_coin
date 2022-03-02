import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import Tuple
from dal.blockchain_tx_db.tx_data_manager_sql import TransactionDataManager
from dal.utils.exceptions import TxDatabaseException
from fastapi import status

class TxGetter():
    def __init__(self) -> None:
        self.tx_db = TransactionDataManager()

    
    def get_tx_by_txid(self, txid: str) -> Tuple:
        try:
            tx = self.tx_db.get_tx_by_txid(txid=txid)
            return (status.HTTP_200_OK, tx)
        except TxDatabaseException:
            return (status.HTTP_404_NOT_FOUND, None)

    
    def get_txs_by_block_hash(self, block_hash: str) -> Tuple:
        try:
            tx_list_of_dicts = self.tx_db.get_txs_by_block_hash(block_hash=block_hash)
            return (status.HTTP_200_OK, tx_list_of_dicts)
        except TxDatabaseException:
            return (status.HTTP_404_NOT_FOUND, None)
