import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import Tuple
from dal.tx_pool_db.tx_pool_data_manager_sql import TxPoolDataManager
from dal.utils.exceptions import TxPoolDatabaseException
from fastapi import status

class TxPoolManager:
    def __init__(self) -> None:
        self.tx_pool_db = TxPoolDataManager()


    def get_tx_by_txid(self, txid: str) -> Tuple:
        try:
            tx = self.tx_pool_db.get_tx_by_txid(txid=txid)
            return (status.HTTP_200_OK, tx)
        except TxPoolDatabaseException:
            return (status.HTTP_404_NOT_FOUND, None)


    def get_top_100_txs(self) -> Tuple:
        try:
            tx_list_of_dicts = self.tx_pool_db.get_top_100_txs()
            return (status.HTTP_200_OK, tx_list_of_dicts)
        except TxPoolDatabaseException:
            return (status.HTTP_200_OK, None) # An empty list is fine, no 404 is required
