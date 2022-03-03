import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import Dict, List
from dal.utxo_db.utxo_data_manager_interface import NodeUtxoInterface
from bl.transaction import Transaction
from dal.sql_database_connection import database_connection
from dal.utils.exceptions import BlockchainDatabaseException

class UtxoDataManager(NodeUtxoInterface):

    def __init__(self) -> None:
        self.db_connection = database_connection


    def get_utxo_by_txid(self, txid: str) -> Dict:
        self.db_connection.cursor.execute(
            """ SELECT txid, vout_addr, vchange_addr FROM node_utxo WHERE utxo=%s""",
            vars=(txid,)
        )

        utxo = self.db_connection.cursor.fetchone()

        if utxo != None:
            return dict(utxo)
        else:
            raise BlockchainDatabaseException(f"No such utxo exists with txid {txid}")

    
    def get_utxos_by_addr(self, addr: str) -> List[Dict]:
        pass


    def add_new_utxo(self, utxo: Transaction) -> None:
        pass


    def update_utxo_by_txid(self, txid: str, utxo: Transaction) -> None:
        pass


    def delete_utxo_by_txid(self, txid: str) -> None:
        pass

