import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from hashlib import sha256
from typing import Dict, List
import pytest
from node.bl.exceptions import BlockException
from node.bl.transaction import Transaction


@pytest.fixture
def test_transaction() -> Transaction:
    vin = [{
        "vin_addr": "1VayNert3x1KzbpzMGt2qdqrAThiRovi8",
        "vin_value": 627907074,
        "vin_script": "3046022100cf19e206eb882624d9631a443eaf4925894" + \
            "3040e9c680bf054881e548606ee77022100a1d624adf36015bfb772171046b" + \
            "1aa2edbed7c1fd20ec8c57fabaaebf0312bed01"
    }]

    return Transaction(tx_block_hash="00000000000009dff396a335faf0c7a834b5543bd63267bb4d7ecf53fb36377e",
                       tx_block_index=4,
                       vin=vin,
                       vout_addr="1Bpqjnfrp4BKxdGFKs1akUzzqxAEW6dVBU",
                       vout_value=90000000,
                       vout_script="76bd7e03396843873ceda9815b392e5bab45b330",
                       vchange_addr="1VayNert3x1KzbpzMGt2qdqrAThiRovi8",
                       vchange_value=537907074,
                       vchange_script="04a39b9e4fbd213ef24bb9be69de4a118dd0644082e47c01fd9159d38637b83f" + \
                       "bcdc115a5d6e970586a012d1cfe3e3a8b1a3d04e763bdc5a071c0e827c0bd834a5")


@pytest.fixture
def test_vin() -> List[Dict]:
    return [{
        "vin_addr": "1VayNert3x1KzbpzMGt2qdqrAThiRovi8",
        "vin_value": 627907074,
        "vin_script": "3046022100cf19e206eb882624d9631a443eaf4925894" + \
            "3040e9c680bf054881e548606ee77022100a1d624adf36015bfb772171046b" + \
            "1aa2edbed7c1fd20ec8c57fabaaebf0312bed01"
    }]


def test_flatten_vin_values_to_str_func(test_vin):
    assert Transaction.flatten_vin_values_to_str(test_vin) == \
        test_vin[0]['vin_addr'] + str(test_vin[0]['vin_value']) + test_vin[0]['vin_script']


def test_flatten_vin_values_to_str_hardcoded(test_vin):
    assert Transaction.flatten_vin_values_to_str(test_vin) == "1VayNert3x1KzbpzMGt2qdqrAThiRovi86279070743046022100cf1" + \
            "9e206eb882624d9631a443eaf49258943040e9c680bf054881e548606ee77022100a1d624adf36015bfb772171046b" + \
            "1aa2edbed7c1fd20ec8c57fabaaebf0312bed01"


def test_calculate_txid_hash(test_transaction: Transaction):
    vin_str = "1VayNert3x1KzbpzMGt2qdqrAThiRovi86279070743046022100cf19e206eb882624d9631a443eaf4925894" + \
        "3040e9c680bf054881e548606ee77022100a1d624adf36015bfb772171046b1aa2edbed7c1fd20ec8c57fabaaebf0312bed01"
    vout_addr = "1Bpqjnfrp4BKxdGFKs1akUzzqxAEW6dVBU"
    vout_script = "76bd7e03396843873ceda9815b392e5bab45b330"
    vchange_addr = "1VayNert3x1KzbpzMGt2qdqrAThiRovi8"
    vchange_script = "04a39b9e4fbd213ef24bb9be69de4a118dd0644082e47c01fd9159d38637b83f" + \
        "bcdc115a5d6e970586a012d1cfe3e3a8b1a3d04e763bdc5a071c0e827c0bd834a5"

    m = sha256()
    m.update(str.encode(vin_str + vout_addr +
             vout_script + vchange_addr + vchange_script))

    assert test_transaction.txid == m.hexdigest()

