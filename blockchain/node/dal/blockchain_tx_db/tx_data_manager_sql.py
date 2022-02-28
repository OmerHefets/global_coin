import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import Dict
from dal.blockchain_tx_db.tx_data_manager_interface import NodeTransactionInterface
from bl.transaction import Transaction
from dal.sql_database_connection import DatabaseConnection

class TransactionDataManager(NodeTransactionInterface):

    def __init__(self) -> None:
        self.db_connection = DatabaseConnection()


    def get_tx_by_hash(self, hash: str) -> Dict:
        self.db_connection.cursor.execute(
            """ SELECT * FROM node_transactions WHERE txid=%s""",
            vars=(hash,)
        )

        tx = dict(self.db_connection.cursor.fetchone())

        return tx

    def get_tx_by_block_hash(self, block_hash: str) -> Dict:
        pass

    def set_new_tx(self, tx: Transaction) -> None:
        pass

    def update_tx_by_hash(self, hash: str, tx: Transaction) -> None:
        pass

    def delete_tx_by_hash(self, hash: str) -> None:
        pass