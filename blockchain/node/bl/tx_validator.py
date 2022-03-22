import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import Dict
from functools import reduce
from blockchain.node.bl.transaction import Transaction
from node.bl.exceptions import TransactionValidationException
from dal.blockchain_tx_db.tx_data_manager_sql import TransactionDataManager


class TxValidator:
    # TODO: Changes in the UTXO db and maybe in VIN as well
    def validate_tx(tx: Transaction) -> bool:
        # check all vin tx's are UTXO
        # check the unlocking script is valid for each vin
        # check tx hash is valid
        # check the inputs == outputs
        pass

    def __validate_vin_is_utxo(tx: Transaction) -> bool:
        # for each vin do "validate_input_is_utxo"
        pass

    def __validate_input_is_utxo(vin_dict: Dict) -> bool:
        # get txid from the vin and address
        # check this txid with address exists
        pass 

    def __validate_scripts_in_vin(tx: Transaction) -> bool:
        # for each vin do "validate_vin_input"
        pass

    def __validate_vin_input(vin_dict: Dict) -> bool:
        vin_txid = vin_dict['txid']

        tx_data_manager = TransactionDataManager()
        tx_data_manager.get_tx_by_txid(vin_txid)

        
        # get tx by the txid of the vin (from tx db)
        # find address and save its output script as the message
        # validate vin script as the valid signature of the message
        pass

    def __validate_tx_hash(tx: Transaction) -> bool:
        expected_hash = tx.calculate_txid_hash()

        if tx.txid != expected_hash:
            raise TransactionValidationException("TX hash is not valid.")

        return True

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
