import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import pytest
from node.bl.tx_validator import TxValidator
from node.bl.exceptions import TransactionValidationException
from node.bl.transaction import Transaction
from node.bl.unified_block import UnifiedBlock

@pytest.fixture
def tx_validator() -> TxValidator:
    return TxValidator()

@pytest.fixture
def valid_tx() -> Transaction:
    vin_tx = [{
        "txid": "9a2041052acbcba2875ab048d28ca372a964266cca046d7f2f00655969036e6b",
        "vin_addr": "coinbase",
        "vin_value": 6000,
        "vin_script": "a0a0a0a0a0a0a0a0a0"
    }]

    tx = Transaction(tx_block_hash="00000000000000027e7ba6fe7bad39faf3b5a83daed765f05f7d1b71a1632249",
                        tx_block_index=1,
                        vin=vin_tx,
                        vout_addr="1Bpqjnfrp4BKxdGFKs1akUzzqxAEW6dVBU",
                        vout_value=6000,
                        vchange_addr="1Bpqjnfrp4BKxdGFKs1akUzzqxAEW6dVBU",
                        vchange_value=0)

    return tx

@pytest.fixture
def valid_adv_tx() -> Transaction:
    vin_tx = [{
        "txid": "9a2041052acbcba2875ab048d28ca372a964266cca046d7f2f00655969036e6b",
        "vin_addr": "1VayNert3x1KzbpzMGt2qdqrAThiRov55",
        "vin_value": 627907074,
        "vin_script": "3046022100cf19e206eb882624d9631a443eaf4925894" + \
            "3040e9c680bf054881e548606ee77022100a1d6a24adf36015bfb7721ab4352efab4349456683ab4710"
    },
    {
        "txid": "9a2041052acbcba2875ab048d28ca372a964266cca046d7f2f00655969036e6b",
        "vin_addr": "1VayNert3x1KzbpzMGt2qdqrAThiRov55",
        "vin_value": 120000000,
        "vin_script": "3046022100cf19e206eb882624d9631a443eaf4925894" + \
            "3040e9c680bf054881e548606ee77022100a1d6a24adf36015bfb7721ab4352efab4349456683ab4710"
    }]

    tx = Transaction(tx_block_hash="00000000000000027e7ba6fe7bad39faf3b5a83daed765f05f7d1b71a1632249",
                        tx_block_index=2,
                        vin=vin_tx,
                        vout_addr="1Bpqjnfrp4BKxdGFKs1akUzzqxAEW6dVBU",
                        vout_value=90000000,
                        vchange_addr="1VayNert3x1KzbpzMGt2qdqrAThiRovi8",
                        vchange_value=537907074)

    return tx

@pytest.mark.parametrize(
    argnames="tx",
    argvalues=[("valid_tx"),
               ("valid_adv_tx")]
)
def test_calc_tx_sum_of_outputs(tx_validator, tx, request):
    tx = request.getfixturevalue(tx)
    assert tx.vout_value + tx.vchange_value == tx_validator._TxValidator__calc_tx_sum_of_outputs(tx)


@pytest.mark.parametrize(
    argnames=["tx","input_val"],
    argvalues=[("valid_tx", 6000),
               ("valid_adv_tx", 747907074)]
)
def test_calc_tx_sum_of_inputs(tx_validator, tx, input_val, request):
    tx = request.getfixturevalue(tx)
    assert tx_validator._TxValidator__calc_tx_sum_of_inputs(tx) == input_val