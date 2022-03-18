import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from blockchain.node.bl.transaction import Transaction


class TxValidator:
    # TODO: Changes in the UTXO db and maybe in VIN as well
    def validate_tx(tx: Transaction) -> bool:
        # check all vin tx's are UTXO
        # check the unlocking script is valid
        # check the inputs == outputs
        pass

    def __validate_vin_dict_schema():
        pass