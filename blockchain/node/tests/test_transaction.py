import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from hashlib import sha256
from typing import Dict, List
import pytest
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
                       vchange_addr="1VayNert3x1KzbpzMGt2qdqrAThiRovi8",
                       vchange_value=537907074)


@pytest.fixture
def test_advanced_tx() -> Transaction:
    vin = [{
        "vin_addr": "1VayNert3x1KzbpzMGt2qdqrAThiRov55",
        "vin_value": 627907074,
        "vin_script": "3046022100cf19e206eb882624d9631a443eaf4925894" + \
            "3040e9c680bf054881e548606ee77022100a1d624adf36015bfb772171046b" + \
            "1aa2edbed7c1fd20ec8c57fabaaebf031266666"
    },
    {
        "vin_addr": "1VayNert3x1KzbpzMGt2qdqrAThiRov55",
        "vin_value": 120000000,
        "vin_script": "3046022100cf19e206eb882624d9631a443eaf4925894" + \
            "3040e9c680bf054881e548606ee77022100a1d624adf36015bfb772171046b" + \
            "1aa2edbed7c1fd20ec8c57fabaaebf03555"
    }]

    return Transaction(tx_block_hash="00000000000009dff396a335faf0c7a834b5543bd63267bb4d7ecf53fb36377e",
                       tx_block_index=5,
                       vin=vin,
                       vout_addr="1Bpqjnfrp4BKxdGFKs1akUzzqxAEW6dVBU",
                       vout_value=650000000,
                       vchange_addr="1VayNert3x1KzbpzMGt2qdqrAThiRov55",
                       vchange_value=97907074)


@pytest.fixture
def test_vin() -> List[Dict]:
    return [{
        "vin_addr": "1VayNert3x1KzbpzMGt2qdqrAThiRovi8",
        "vin_value": 627907074,
        "vin_script": "3046022100cf19e206eb882624d9631a443eaf4925894" + \
            "3040e9c680bf054881e548606ee77022100a1d624adf36015bfb772171046b" + \
            "1aa2edbed7c1fd20ec8c57fabaaebf0312bed01"
    }]


@pytest.fixture
def test_advanced_vin() -> List[Dict]:
    return [{
        "vin_addr": "1VayNert3x1KzbpzMGt2qdqrAThiRov55",
        "vin_value": 627907074,
        "vin_script": "3046022100cf19e206eb882624d9631a443eaf4925894" + \
            "3040e9c680bf054881e548606ee77022100a1d624adf36015bfb772171046b" + \
            "1aa2edbed7c1fd20ec8c57fabaaebf031266666"
    },
    {
        "vin_addr": "1VayNert3x1KzbpzMGt2qdqrAThiRov55",
        "vin_value": 120000000,
        "vin_script": "3046022100cf19e206eb882624d9631a443eaf4925894" + \
            "3040e9c680bf054881e548606ee77022100a1d624adf36015bfb772171046b" + \
            "1aa2edbed7c1fd20ec8c57fabaaebf03555"
    }]


def test_flatten_vin_values_to_str_func(test_vin):
    assert Transaction.flatten_vin_values_to_str(test_vin) == \
        test_vin[0]['vin_addr'] + str(test_vin[0]['vin_value']) + test_vin[0]['vin_script']


def test_flatten_vin_values_to_str_hardcoded(test_vin):
    assert Transaction.flatten_vin_values_to_str(test_vin) == "1VayNert3x1KzbpzMGt2qdqrAThiRovi86279070743046022100cf1" + \
            "9e206eb882624d9631a443eaf49258943040e9c680bf054881e548606ee77022100a1d624adf36015bfb772171046b" + \
            "1aa2edbed7c1fd20ec8c57fabaaebf0312bed01"


def test_flatten_vin_values_to_str_func_adv(test_advanced_vin):
    assert Transaction.flatten_vin_values_to_str(test_advanced_vin) == \
        test_advanced_vin[0]['vin_addr'] + str(test_advanced_vin[0]['vin_value']) + test_advanced_vin[0]['vin_script'] + \
        test_advanced_vin[1]['vin_addr'] + str(test_advanced_vin[1]['vin_value']) + test_advanced_vin[1]['vin_script']


def test_flatten_vin_values_to_str_hardcoded_adv(test_advanced_vin):
    assert Transaction.flatten_vin_values_to_str(test_advanced_vin) == "1VayNert3x1KzbpzMGt2qdqrAThiRov556279070743046022100cf1" + \
            "9e206eb882624d9631a443eaf49258943040e9c680bf054881e548606ee77022100a1d624adf36015bfb772171046b" + \
            "1aa2edbed7c1fd20ec8c57fabaaebf031266666" + "1VayNert3x1KzbpzMGt2qdqrAThiRov55120000000" + \
            "3046022100cf19e206eb882624d9631a443eaf4925894" + \
            "3040e9c680bf054881e548606ee77022100a1d624adf36015bfb772171046b" + \
            "1aa2edbed7c1fd20ec8c57fabaaebf03555"


def test_calculate_txid_hash(test_transaction: Transaction):
    vin_str = "1VayNert3x1KzbpzMGt2qdqrAThiRovi86279070743046022100cf19e206eb882624d9631a443eaf4925894" + \
        "3040e9c680bf054881e548606ee77022100a1d624adf36015bfb772171046b1aa2edbed7c1fd20ec8c57fabaaebf0312bed01"
    vout_addr = "1Bpqjnfrp4BKxdGFKs1akUzzqxAEW6dVBU"
    vchange_addr = "1VayNert3x1KzbpzMGt2qdqrAThiRovi8"

    m = sha256()
    m.update(str.encode(vin_str + vout_addr + vchange_addr))

    assert test_transaction.txid == m.hexdigest()


def test_encode_tx_vin_length(test_transaction: Transaction):
    assert len(test_transaction.encode_tx_vin()) == 250 # a single vin


def test_encode_tx_vin_hardcoded(test_transaction: Transaction):
    assert test_transaction.encode_tx_vin() == "00000001VayNert3x1KzbpzMGt2qdqrAThiRovi" + \
    "8000000000000000000000627907074" + \
    "00000000000000000000000000000000003046022100cf19e206eb882624d9631a443eaf49258943040e9c680bf05" + \
    "4881e548606ee77022100a1d624adf36015bfb772171046b1aa2edbed7c1fd20ec8c57fabaaebf0312bed01"


def test_encode_tx_vin_length_adv(test_advanced_tx: Transaction):
    assert len(test_advanced_tx.encode_tx_vin()) == 500 # 2 vin's


def test_encode_tx_vin_hardcoded_adv(test_advanced_tx: Transaction):
    assert test_advanced_tx.encode_tx_vin() == "00000001VayNert3x1KzbpzMGt2qdqrAThiRov55" + \
    "000000000000000000000627907074" + \
    "00000000000000000000000000000000003046022100cf19e206eb882624d9631a443eaf4925894" + \
    "3040e9c680bf054881e548606ee77022100a1d624adf36015bfb772171046b" + \
    "1aa2edbed7c1fd20ec8c57fabaaebf031266666" + \
    "00000001VayNert3x1KzbpzMGt2qdqrAThiRov55" + \
    "000000000000000000000120000000" + \
    "000000000000000000000000000000000000003046022100cf19e206eb882624d9631a443eaf4925894" + \
    "3040e9c680bf054881e548606ee77022100a1d624adf36015bfb772171046b" + \
    "1aa2edbed7c1fd20ec8c57fabaaebf03555"


def test_decode_tx_vin_adv(test_advanced_tx: Transaction):
    encoded_vin = test_advanced_tx.encode_tx_vin()
    decoded_vin = test_advanced_tx.decode_tx_vin(encoded_vin=encoded_vin)
    assert decoded_vin == test_advanced_tx.vin