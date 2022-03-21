import sys
import os
from typing import Dict
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from blockchain.node.bl.transaction import Transaction
from node.bl.exceptions import TransactionValidationException


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
        # get tx by the txid of the vin (from tx db)
        # find address and save its output script as the message
        # validate vin script as the valid signature of the message
        pass

    def __validate_tx_hash(tx: Transaction) -> bool:
        # expected_hash = tx.calc_hash()
        # validate expected_hash == tx.hash
        pass

    def __validate_input_val_equals_output(tx: Transaction) -> bool:
        # check if sum_inputs == sum_outputs - return true if valid, or 
        # TransactionValidationException otherwise
        pass

    def __calc_tx_sum_of_inputs(tx: Transaction) -> int:
        # for each input in tx.vin, sum all input_value field
        pass

    @staticmethod
    def __calc_tx_sum_of_outputs(tx: Transaction) -> int:
        return tx.vchange_value + tx.vout_value