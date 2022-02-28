import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import Dict
from dal.blockchain_db.blockchain_data_manager_interface import NodeBlockchainInterface
from bl.block import Block
from dal.sql_database_connection import DatabaseConnection
from datetime import datetime


class BlockchainDataManager(NodeBlockchainInterface):
    
    def __init__(self) -> None:
        self.db_connection = DatabaseConnection()


    def get_block_by_hash(self, hash: str) -> Dict:
        self.db_connection.cursor.execute(
            """ SELECT * FROM node_blockchain WHERE hash=%s""",
            vars=(hash,)
        )

        block: Dict = dict(self.db_connection.cursor.fetchone())

        return block

    def get_block_by_height(self, height: int) -> Dict:
        self.db_connection.cursor.execute(
            """ SELECT * FROM node_blockchain WHERE height=%s""",
            vars=(str(height),)
        )

        block: Dict = dict(self.db_connection.cursor.fetchone())

        return block

    def add_new_block(self, block: Block) -> None:
        self.db_connection.cursor.execute(
            """ INSERT INTO node_blockchain 
            (hash, prev_block_hash, merkle_root, difficulty, nonce, height, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            vars=(block.hash, block.prev_block_hash, block.merkle_root, str(block.difficulty), 
            str(block.nonce), str(block.height), str(block.timestamp))
        )

        self.db_connection.conn.commit()

    def update_block_by_hash(self, hash: str, block: Block) -> None:
        self.db_connection.cursor.execute(
            """ UPDATE node_blockchain SET
            hash = %s, prev_block_hash = %s, merkle_root = %s, difficulty = %s,
            nonce = %s, height = %s, timestamp = %s WHERE hash=%s""",
            vars=(block.hash, block.prev_block_hash, block.merkle_root, str(block.difficulty), 
            str(block.nonce), str(block.height), str(block.timestamp), hash)
        )

        self.db_connection.conn.commit()

    def delete_block_by_hash(self, hash: str) -> None:
        self.db_connection.cursor.execute(
            """ DELETE FROM node_blockchain WHERE hash=%s""",
            vars=(hash,)
        )

        self.db_connection.conn.commit()
