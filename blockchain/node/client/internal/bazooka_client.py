from ast import Pass
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from node.bl.transaction import Transaction
from node.bl.unified_block import UnifiedBlock
from node.bl.block import Block
from node.bl.node_managers.blockchain_manager import BlockchainManager
from node.bl.node_managers.tx_manager import TxManager
from node.bl.node_managers.tx_pool_manager import TxPoolManager
from node.bl.node_managers.utxo_manager import UtxoManager
from node.dal.blockchain_db.blockchain_data_manager_sql import BlockchainDataManager
from node.dal.blockchain_tx_db.tx_data_manager_sql import TransactionDataManager
from node.dal.tx_pool_db.tx_pool_data_manager_sql import TxPoolDataManager
from node.dal.utxo_db.utxo_data_manager_sql import UtxoDataManager

class BazookaClient:

    def __init__(self) -> None:
        self.blockchain_data_manager = BlockchainDataManager()
        self.blockchain_manager = BlockchainManager()
        self.tx_data_manager = TransactionDataManager()
        self.tx_manager = TxManager()
        self.tx_pool_data_manager = TxPoolDataManager()
        self.tx_pool_manager = TxPoolManager()
        self.utxo_data_manager = UtxoDataManager()
        self.utxo_manager = UtxoManager()


    def insert_new_unified_block(self, unified_block: UnifiedBlock) -> None:
        self.__insert_new_block(unified_block=unified_block)

        for tx in unified_block.tx_list:
            self.tx_data_manager.set_new_tx(tx=tx)

 
    def __insert_new_block(self, unified_block: UnifiedBlock) -> None:
        block = Block(hash=unified_block.hash,
                      prev_block_hash=unified_block.prev_block_hash,
                      merkle_root=unified_block.merkle_root,
                      timestamp=unified_block.timestamp,
                      difficulty=unified_block.difficulty,
                      nonce=unified_block.nonce,
                      height=unified_block.height)

        self.blockchain_data_manager.add_new_block(block=block)

    
    def remove_txs_in_block_from_tx_pool(self, unified_block: UnifiedBlock) -> None:
        tx_list_without_coinbase_tx = list(filter(lambda tx: tx.tx_block_index != 1, unified_block.tx_list))
        
        for tx in tx_list_without_coinbase_tx:
            self.tx_pool_data_manager.delete_tx_by_txid(txid=tx.txid)


    def remove_txs_in_block_from_utxo(self, unified_block: UnifiedBlock) -> None:
        tx_list_without_coinbase_tx = list(filter(lambda tx: tx.tx_block_index != 1, unified_block.tx_list))

        for tx in tx_list_without_coinbase_tx:
            self.__remove_vin_utxos_from_db(tx=tx)


    def __remove_vin_utxos_from_db(self, tx: Transaction) -> None:
        for vin_input in tx.vin:
            addr = vin_input['vin_addr']
            txid = vin_input['txid']

            self.utxo_data_manager.delete_utxo_by_txid_and_addr(txid=txid, addr=addr)


    def update_new_utxos(self, unified_block: UnifiedBlock) -> None:
        for tx in unified_block.tx_list:
            self.__update_tx_outputs_as_utxos(tx=tx)


    def __update_tx_outputs_as_utxos(self, tx: Transaction) -> None:
        self.utxo_data_manager.add_new_utxo(txid=tx.txid, vout_addr=tx.vout_addr, vchange_addr='0')
        if tx.vchange_value > 0: # if change does not exist, do not add it to the UTXO DB
            self.utxo_data_manager.add_new_utxo(txid=tx.txid, vout_addr='0', vchange_addr=tx.vchange_addr)