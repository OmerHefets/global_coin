import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import Dict
from dal.blockchain_db.blockchain_data_manager_interface import NodeBlockchainInterface
from bl.block import Block
from dal.sql_database_connection import database_connection
from dal.utils.exceptions import BlockchainDatabaseException

class BlockchainDataManager(NodeBlockchainInterface):
    
    def __init__(self) -> None:
        self.db_connection = database_connection


    def get_latest_block(self) -> Dict:
        self.db_connection.cursor.execute(
            """ SELECT hash, prev_block_hash, merkle_root, nonce, height, difficulty, timestamp FROM node_blockchain
                WHERE height = (SELECT MAX(height) FROM node_blockchain)"""
        )

        block = self.db_connection.cursor.fetchone()

        if block != None:
            return dict(block)
        else:
            raise BlockchainDatabaseException(f"Not a single block exists in the blockchain.")


    def get_block_by_hash(self, hash: str) -> Dict:
        self.db_connection.cursor.execute(
            """ SELECT hash, prev_block_hash, merkle_root, nonce, height,
            difficulty, timestamp FROM node_blockchain WHERE hash=%s""",
            vars=(hash,)
        )

        block = self.db_connection.cursor.fetchone()

        if block != None:
            return dict(block)
        else:
            raise BlockchainDatabaseException(f"Not a valid block hash {hash}")


    def get_block_by_height(self, height: int) -> Dict:
        self.db_connection.cursor.execute(
            """ SELECT hash, prev_block_hash, merkle_root, nonce, height,
            difficulty, timestamp FROM node_blockchain WHERE height=%s""",
            vars=(str(height),)
        )

        block = self.db_connection.cursor.fetchone()

        if block != None:
            return dict(block)
        else:
            raise BlockchainDatabaseException(f"Not a valid block height {str(height)}")


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


# dbm = BlockchainDataManager()
# dbm.get_block_by_height(24235)