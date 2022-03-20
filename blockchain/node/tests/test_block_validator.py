import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import pytest
from node.bl.block_validator import BlockValidator
from node.bl.transaction import Transaction
from node.bl.unified_block import UnifiedBlock
from node.bl.exceptions import BlockValidationException
from datetime import datetime, timedelta

@pytest.fixture
def bv() -> BlockValidator:
    return BlockValidator()

@pytest.fixture
def unified_block() -> UnifiedBlock:
    vin_tx1 = [{
        "txid": "9a2041052acbcba2875ab048d28ca372a964266cca046d7f2f00655969036e6b",
        "vin_addr": "coinbase",
        "vin_value": 6000,
        "vin_script": "a0a0a0a0a0a0a0a0a0"
    }]

    tx_1 = Transaction(tx_block_hash="00000000000000027e7ba6fe7bad39faf3b5a83daed765f05f7d1b71a1632249",
                        tx_block_index=1,
                        vin=vin_tx1,
                        vout_addr="1Bpqjnfrp4BKxdGFKs1akUzzqxAEW6dVBU",
                        vout_value=6000,
                        vchange_addr="1Bpqjnfrp4BKxdGFKs1akUzzqxAEW6dVBU",
                        vchange_value=0)
    
    vin_tx2 = [{
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

    tx_2 = Transaction(tx_block_hash="00000000000000027e7ba6fe7bad39faf3b5a83daed765f05f7d1b71a1632249",
                        tx_block_index=2,
                        vin=vin_tx2,
                        vout_addr="1Bpqjnfrp4BKxdGFKs1akUzzqxAEW6dVBU",
                        vout_value=90000000,
                        vchange_addr="1VayNert3x1KzbpzMGt2qdqrAThiRovi8",
                        vchange_value=537907074)

    unified_b = UnifiedBlock(hash="00000000000000027e7ba6fe7bad39faf3b5a83daed765f05f7d1b71a1632249",
                    prev_block_hash="00000000000000027e7ba6fe7bad39faf3b5a83daed765f05f7d173951632249",
                    merkle_root="5e049f4030e0ab2debb92378f53c0a6e09548aea083f3ab25e1d94ea1155e29d",
                    timestamp=datetime.timestamp(
                        datetime.now()),
                    difficulty=180923195.25802612,
                    nonce=4215469401,
                    height=124193,
                    tx_list=[tx_1, tx_2])

    return unified_b

@pytest.fixture
def wrong_unified_block() -> UnifiedBlock:
    vin_tx1 = [{
        "txid": "9a2041052acbcba2875ab048d28ca372a964266cca046d7f2f00655969036e6b",
        "vin_addr": "1VayNert3x1KzbpzMGt2qdqrAThiRov55",
        "vin_value": 6000,
        "vin_script": "a0a0a0a0a0a0a0a0a0"
    }]

    tx_1 = Transaction(tx_block_hash="00000000000009dff396a335faf0c7a834b5543bd63267bb4d7ecf53fb36377e",
                        tx_block_index=1,
                        vin=vin_tx1,
                        vout_addr="1Bpqjnfrp4BKxdGFKs1akUzzqxAEW6dVBU",
                        vout_value=6000,
                        vchange_addr="1Bpqjnfrp4BKxdGFKs1akUzzqxAEW6dVBU",
                        vchange_value=0)
    
    vin_tx2 = [{
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

    tx_2 = Transaction(tx_block_hash="00000000000009dff396a335faf0c7a834b5543bd63267bb4d7ecf53fb36377e",
                        tx_block_index=2,
                        vin=vin_tx2,
                        vout_addr="1Bpqjnfrp4BKxdGFKs1akUzzqxAEW6dVBU",
                        vout_value=90000000,
                        vchange_addr="1VayNert3x1KzbpzMGt2qdqrAThiRovi8",
                        vchange_value=537907074)

    unified_b = UnifiedBlock(hash="00000000000000027e7ba6fe7bad39faf3b5a83daed765f05f7d1b71a1632249",
                    prev_block_hash="00000000000000027e7ba6fe7bad39faf3b5a83daed765f05f7d173951632249",
                    merkle_root="5e049f4030e0ab2debb92378f53c0a6e09548aea083f3ab25e1d94ea1155e29d",
                    timestamp=datetime.timestamp(
                        datetime.now()),
                    difficulty=180923195.25802612,
                    nonce=4215469401,
                    height=124193,
                    tx_list=[tx_1, tx_2])

    return unified_b


def test_validate_first_tx(unified_block, bv):
    assert bv._BlockValidator__validate_first_tx(unified_block.tx_list) == True


def test_validate_first_tx_wrong(wrong_unified_block, bv):
    with pytest.raises(BlockValidationException):
        bv._BlockValidator__validate_first_tx(wrong_unified_block.tx_list)


def test_validate_txs_related_to_block(unified_block, bv):
    assert bv._BlockValidator__validate_txs_related_to_block(unified_block) == True


def test_validate_txs_related_to_block_wrong(wrong_unified_block, bv):
    with pytest.raises(BlockValidationException):
            bv._BlockValidator__validate_txs_related_to_block(wrong_unified_block)


def test_validate_merkle_root(unified_block, bv):
    assert bv._BlockValidator__validate_merkle_root(unified_block) == True


def test_validate_merkle_root_wrong(unified_block, bv):
    unified_block.merkle_root = "wrong_merkle_root"
    with pytest.raises(BlockValidationException):
        bv._BlockValidator__validate_merkle_root(unified_block)


@pytest.mark.parametrize(argnames="req_difficulty",
                         argvalues=[0, 1.3, 10, -2])
def test_validate_block_hash_val_by_difficulty(unified_block, bv, req_difficulty):
    assert bv._BlockValidator__validate_block_hash_val_by_difficulty(unified_block, req_difficulty) == True


@pytest.mark.parametrize(argnames="req_difficulty",
                         argvalues=[75, 100, 256, 400, 1000])
def test_validate_block_hash_val_by_difficulty_invalid_diff(unified_block, bv, req_difficulty):
    assert bv._BlockValidator__validate_block_hash_val_by_difficulty(unified_block, req_difficulty) == False