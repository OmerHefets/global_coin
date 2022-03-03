import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import Dict, List
from dal.blockchain_tx_db.tx_data_manager_interface import NodeTransactionInterface
from bl.transaction import Transaction
from dal.sql_database_connection import database_connection
from dal.utils.exceptions import TxDatabaseException

class TransactionDataManager(NodeTransactionInterface):

    def __init__(self) -> None:
        self.db_connection = database_connection


    def get_tx_by_txid(self, txid: str) -> Dict:
        self.db_connection.cursor.execute(
            """ SELECT txid, tx_block_hash, tx_block_index, vin, 
            vout_addr, vout_value, vout_script, vchange_addr, vchange_value, vchange_script
            FROM node_transactions WHERE txid=%s""",
            vars=(txid,)
        )

        tx = self.db_connection.cursor.fetchone()

        if tx != None:
            return dict(tx)
        else:
            raise TxDatabaseException(f"Not a valid tx txid {txid}")


    def get_txs_by_block_hash(self, block_hash: str) -> Dict:
        self.db_connection.cursor.execute(
            """ SELECT txid, tx_block_hash, tx_block_index, vin, 
            vout_addr, vout_value, vout_script, vchange_addr, vchange_value, vchange_script
            FROM node_transactions WHERE tx_block_hash=%s""",
            vars=(block_hash,)
        )

        tx_list = self.db_connection.cursor.fetchall()

        if len(tx_list) != 0:
            tx_list_of_dicts: List[Dict] = [dict(tx) for tx in list(tx_list)]
            return tx_list_of_dicts
        else:
            raise TxDatabaseException(f"No transactions exist for this hash {block_hash}")


    def set_new_tx(self, tx: Transaction) -> None:
        self.db_connection.cursor.execute(
            """ INSERT INTO node_transactions
            (txid, tx_block_hash, tx_block_index, vin, 
            vout_addr, vout_value, vout_script,
            vchange_addr, vchange_value, vchange_script)

            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            vars=(tx.txid, tx.tx_block_hash, str(tx.tx_block_index), tx.encode_tx_vin(), 
            tx.vout_addr, str(tx.vout_value), tx.vout_script,
            tx.vchange_addr, str(tx.vchange_value), tx.vchange_script) 
        )

        self.db_connection.conn.commit()


    def update_tx_by_txid(self, txid: str, tx: Transaction) -> None:
        self.db_connection.cursor.execute(
            """ UPDATE node_transactions SET
            txid = %s, tx_block_hash = %s, tx_block_index = %s, vin = %s, 
            vout_addr = %s, vout_value = %s, vout_script = %s, 
            vchange_addr = %s, vchange_value = %s, vchange_script = %s
            
            WHERE txid = %s""",
            vars=(tx.txid, tx.tx_block_hash, str(tx.tx_block_index), tx.encode_tx_vin(),
            tx.vout_addr, str(tx.vout_value), tx.vout_script, 
            tx.vchange_addr, str(tx.vchange_value), tx.vout_script, txid)
        )

        self.db_connection.conn.commit()


    def delete_tx_by_txid(self, txid: str) -> None:
        self.db_connection.cursor.execute(
            """ DELETE FROM node_transactions WHERE txid = %s""",
            vars=(txid,)
        )
        
        self.db_connection.conn.commit()


# tdm = TransactionDataManager()
# tx_dict = tdm.get_tx_by_txid(txid='a1e1e9761e5fde1dfc626297ff71deea569b6a61fa7e9f9797dcfffa662c381a')
# print(tx_dict)

# print(tdm.get_txs_by_block_hash(block_hash='00000000000000027e7ba6fe7bad39faf3b5a83daed765f05f7d1b71a1632249'))

# vin = [{
#         "vin_addr": "1VayNert3x1KzbpzMGt2qdqrAThiRovi8",
#         "vin_value": 627907074,
#         "vin_script": "3046022100cf19e206eb882624d9631a443eaf4925894" + \
#             "3040e9c680bf054881e548606ee77022100a1d624adf36015bfb772171046b" + \
#             "1aa2edbed7c1fd20ec8c57fabaaebf0312bed01"
#     }]

# tx = Transaction(tx_block_hash="543bd63267bb4d736377e66666666666666666",
#                        tx_block_index=4,
#                        vin=vin,
#                        vout_addr="1BpqjnfKs1akUzzqxAEW6dVBU",
#                        vout_value=90000000,
#                        vout_script="76bd7e03393ceda9815b392e5bab45b330",
#                        vchange_addr="1VayNerGt2qdqrAThiRovi8",
#                        vchange_value=537907074,
#                        vchange_script="04a39b9e4fbd213ef23d04e763bdc5a071c0e827c0bd834a5")


# tdm.update_tx_by_txid(txid='7c084390791c6bb1d39ebb861d072b5cdb075b3fda7344f22cf8b5b43603b40d', tx=tx)

# tdm.delete_tx_by_txid(txid='7c084390791c6bb1d39ebb861d072b5cdb075b3fda7344f22cf8b5b43603b40d')
