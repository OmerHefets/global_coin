from audioop import add
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import Tuple
from dal.utxo_db.utxo_data_manager_sql import UtxoDataManager
from dal.utils.exceptions import UtxoDatabaseException
from fastapi import status

class UtxoManager:
    def __init__(self) -> None:
        self.utxo_db = UtxoDataManager()


    def get_utxo_by_txid(self, txid: str) -> Tuple:
        try:
            utxo = self.utxo_db.get_utxo_by_txid(txid=txid)
            return (status.HTTP_200_OK, utxo)
        except UtxoDatabaseException:
            return (status.HTTP_404_NOT_FOUND, None)

    
    def get_utxos_by_addr(self, addr: str) -> Tuple:
        try:
            utxo_list_of_dicts = self.utxo_db.get_utxos_by_addr(addr=addr)
            return (status.HTTP_200_OK, utxo_list_of_dicts)
        except UtxoDatabaseException:
            return (status.HTTP_200_OK, None) # return 200 for exception since it's possible no UTXO found
