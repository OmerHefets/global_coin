import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import Dict, List
from dal.utxo_db.utxo_data_manager_interface import NodeUtxoInterface
from bl.transaction import Transaction
from dal.sql_database_connection import database_connection
from dal.utils.exceptions import UtxoDatabaseException

class UtxoDataManager(NodeUtxoInterface):

    def __init__(self) -> None:
        self.db_connection = database_connection


    def get_utxo_by_txid(self, txid: str) -> Dict:
        self.db_connection.cursor.execute(
            """ SELECT txid, vout_addr, vchange_addr FROM node_utxo WHERE txid=%s""",
            vars=(txid,)
        )

        utxo = self.db_connection.cursor.fetchone()

        if utxo != None:
            return dict(utxo)
        else:
            raise UtxoDatabaseException(f"No such utxo exists with txid {txid}") 


    def get_utxo_by_txid_and_addr(self, txid: str, addr: str) -> Dict:
        self.db_connection.cursor.execute(
            """ SELECT txid, vout_addr, vchange_addr FROM node_utxo
            WHERE txid=%s AND (vout_addr=%s OR vchange_addr=%s)""",
            vars=(txid, addr, addr)
        )

        utxo = self.db_connection.cursor.fetchone()

        if utxo != None:
            return dict(utxo)
        else:
            raise UtxoDatabaseException(f"No such utxo exists with txid {txid} and addr {addr}")


    def get_utxos_by_addr(self, addr: str) -> List[Dict]:
        self.db_connection.cursor.execute(
            """ SELECT txid, vout_addr, vchange_addr FROM node_utxo
            WHERE vout_addr=%s OR vchange_addr=%s""",
            vars=(addr, addr)
        )

        utxo_list = self.db_connection.cursor.fetchall()

        if len(utxo_list) != 0:
            utxo_list_of_dicts = [dict(utxo) for utxo in list(utxo_list)]
            return utxo_list_of_dicts
        else:
            raise UtxoDatabaseException(f"No utxo's exists for address {addr}")
        

    def add_new_utxo(self, utxo: Transaction) -> None:
        self.db_connection.cursor.execute(
            """INSERT INTO node_utxo (txid, vout_addr, vchange_addr)
            VALUES (%s, %s, %s)""",
            vars=(utxo.txid, utxo.vout_addr, utxo.vchange_addr)
        )

        self.db_connection.conn.commit()


    def update_utxo_by_txid(self, txid: str, utxo: Transaction) -> None:
        self.db_connection.cursor.execute(
            """ UPDATE node_utxo SET
            txid=%s, vout_addr=%s, vchange_addr=%s
            
            WHERE txid=%s""",
            vars=(utxo.txid, utxo.vout_addr, utxo.vchange_addr, txid)
        )

        self.db_connection.conn.commit()


    def delete_utxo_by_txid(self, txid: str) -> None:
        self.db_connection.cursor.execute(
            """ DELETE FROM node_utxo WHERE txid=%s""",
            vars=(txid,)
        )

        self.db_connection.conn.commit()

