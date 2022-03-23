import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import Dict
from functools import reduce
from blockchain.node.bl.transaction import Transaction
from node.bl.exceptions import TransactionValidationException
from node.dal.utils.exceptions import UtxoDatabaseException
from dal.blockchain_tx_db.tx_data_manager_sql import TransactionDataManager
from dal.utxo_db.utxo_data_manager_sql import UtxoDataManager
from codecs import encode, decode
from ecdsa import VerifyingKey


class TxValidator:
    
    def validate_tx(tx: Transaction, pub_key: VerifyingKey) -> bool:
        """
        validate all vin tx's are UTXO
        validate the unlocking script is valid for each vin
        validate tx hash is valid
        validate the inputs == outputs
        """
        return TxValidator.__validate_vin_is_utxo(tx) and TxValidator.__validate_scripts_in_vin(tx, pub_key) \
            and TxValidator.__validate_tx_hash(tx) and TxValidator.__validate_input_val_equals_output(tx)


    def __validate_vin_is_utxo(tx: Transaction) -> bool:
        vins_utxo_validations = [TxValidator.__validate_input_is_utxo(vin_dict) for vin_dict in tx.vin]
        return False if False in vins_utxo_validations else True


    def __validate_input_is_utxo(vin_dict: Dict) -> bool:
        vin_addr = vin_dict['vin_addr']
        vin_txid = vin_dict['txid']

        try:
            utxo_data_manager = UtxoDataManager()
            # Simply call the DB to look for the utxo, no need to store it anywhere
            utxo_data_manager.get_utxo_by_txid_and_addr(txid=vin_txid, addr=vin_addr)
            return True
        except UtxoDatabaseException:
            return False


    def __validate_scripts_in_vin(tx: Transaction, pub_key: VerifyingKey) -> bool:
        # for each vin do "validate_vin_input"
        vins_validations = [TxValidator.__validate_vin_input(vin_dict, pub_key) for vin_dict in tx.vin]
        return False if False in vins_validations else True


    def __validate_vin_input(vin_dict: Dict, pub_key: VerifyingKey) -> bool:
        # get tx by the txid of the vin (from tx db)
        # find address and save its output script as the message
        # validate vin script as the valid signature of the message

        vin_txid = vin_dict['txid']
        vin_address = vin_dict['vin_addr']
        unlocking_script = vin_dict['vin_script']

        tx_data_manager = TransactionDataManager()
        tx: Dict = tx_data_manager.get_tx_by_txid(vin_txid)

        if vin_address == tx['vout_addr']:
            locking_script = tx['vout_script']
            # In real implementation, we would first check that hash(pub_key) == addr
            return pub_key.verify(decode(unlocking_script, 'hex'), encode(locking_script))

        elif vin_address == tx['vchange_addr']:
            locking_script = tx['vchange_script']
            return pub_key.verify(decode(unlocking_script, 'hex'), encode(locking_script))

        else:
            raise TransactionValidationException("No valid address exists for this vin script verification")


    @staticmethod
    def __validate_tx_hash(tx: Transaction) -> bool:
        expected_hash = tx.calculate_txid_hash()

        if tx.txid != expected_hash:
            raise TransactionValidationException("TX hash is not valid.")

        return True

    @staticmethod
    def __validate_input_val_equals_output(tx: Transaction) -> bool:
        if TxValidator.__calc_tx_sum_of_inputs(tx) != TxValidator.__calc_tx_sum_of_outputs(tx):
            raise TransactionValidationException("Inputs and outputs does not sum to the same value.")

        return True


    @staticmethod
    def __calc_tx_sum_of_inputs(tx: Transaction) -> int:
        return reduce(lambda x, y: x+y, map(lambda vin: vin['vin_value'], tx.vin), 0)


    @staticmethod
    def __calc_tx_sum_of_outputs(tx: Transaction) -> int:
        return tx.vchange_value + tx.vout_value
