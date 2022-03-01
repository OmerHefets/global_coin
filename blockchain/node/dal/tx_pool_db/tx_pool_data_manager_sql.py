import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import Dict, List
from dal.tx_pool_db.tx_pool_data_manager_interface import NodeTxPoolInterface
from bl.transaction import Transaction
from dal.sql_database_connection import DatabaseConnection

class TxPoolDataManager(NodeTxPoolInterface):

    def __init__(self) -> None:
        self.db_connection = DatabaseConnection()


    def get_tx_by_txid(self, txid: str) -> Dict:
        self.db_connection.cursor.execute(
            """ SELECT * FROM node_tx_pool WHERE txid = %s""",
            vars=(txid,)
        )

        tx = dict(self.db_connection.cursor.fetchone())

        return tx


    def get_top_100_txs(self) -> List[Dict]:
        self.db_connection.cursor.execute(
            """ SELECT * FROM node_tx_pool LIMIT 100"""
        )

        tx_list = list(self.db_connection.cursor.fetchall())
        tx_list_of_dicts: List[Dict] = [dict(tx) for tx in tx_list]

        return tx_list_of_dicts


    def set_new_tx(self, tx: Transaction) -> None:
        self.db_connection.cursor.execute(
            """ INSERT INTO node_tx_pool
            (txid, vin, 
            vout_addr, vout_value, vout_script,
            vchange_addr, vchange_value, vchange_script)

            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            vars=(tx.txid, tx.encode_tx_vin(), 
            tx.vout_addr, str(tx.vout_value), tx.vout_script,
            tx.vchange_addr, str(tx.vchange_value), tx.vchange_script) 
        )

        self.db_connection.conn.commit()


    def update_tx_by_txid(self, txid: str, tx: Transaction) -> None:
        self.db_connection.cursor.execute(
            """ UPDATE node_tx_pool SET
            txid = %s, vin = %s, 
            vout_addr = %s, vout_value = %s, vout_script = %s, 
            vchange_addr = %s, vchange_value = %s, vchange_script = %s
            
            WHERE txid = %s""",
            vars=(tx.txid, tx.encode_tx_vin(),
            tx.vout_addr, str(tx.vout_value), tx.vout_script, 
            tx.vchange_addr, str(tx.vchange_value), tx.vout_script, txid)
        )

        self.db_connection.conn.commit()


    def delete_tx_by_txid(self, txid: str) -> None:
        self.db_connection.cursor.execute(
            """ DELETE FROM node_tx_pool WHERE txid = %s""",
            vars=(txid,)
        )
        
        self.db_connection.conn.commit()


