from datetime import datetime
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from hashlib import sha256
from typing import Dict, List
import pytest
from node.bl.transaction import Transaction
from node.bl.unified_block import UnifiedBlock


@pytest.fixture
def unified_block() -> UnifiedBlock:
    vin_tx1 = [{
        "txid": "9a2041052acbcba2875ab048d28ca372a964266cca046d7f2f00655969036e6b",
        "vin_addr": "coinbase",
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

    unified_b = UnifiedBlock(hash="00000000000009dff396a335faf0c7a834b5543bd63267bb4d7ecf53fb36377e",
                    prev_block_hash="00000000000000027e7ba6fe7bad39faf3b5a83daed765f05f7d173951632249",
                    merkle_root="6192ee6d7707199544e62f2fb88bc54f6f157f239f8d34802cf41084e2d8b4ad",
                    timestamp=datetime.timestamp(
                        datetime.now()),
                    difficulty=180923195.25802612,
                    nonce=4215469401,
                    height=124193,
                    tx_list=[tx_1, tx_2])

    return unified_b


@pytest.fixture
def unified_block_dict(unified_block: UnifiedBlock) -> Dict:
    return {
        "hash": "00000000000009dff396a335faf0c7a834b5543bd63267bb4d7ecf53fb36377e",
        "prev_block_hash": "00000000000000027e7ba6fe7bad39faf3b5a83daed765f05f7d173951632249",
        "merkle_root": "6192ee6d7707199544e62f2fb88bc54f6f157f239f8d34802cf41084e2d8b4ad",
        "timestamp": unified_block.timestamp,
        "difficulty": 180923195.25802612,
        "nonce": 4215469401,
        "height": 124193,
        "tx_list": [
        {
            "tx_block_hash": "00000000000009dff396a335faf0c7a834b5543bd63267bb4d7ecf53fb36377e",
            "tx_block_index": 2,
            "vin": [{
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
                            "3040e9c680bf054881e548606ee77022100a1d6a24adf36015bfb7721ab4352efab4349456683ab4710"}],
            "vout_addr": "1Bpqjnfrp4BKxdGFKs1akUzzqxAEW6dVBU",
            "vout_value": 650000000,
            "vchange_addr": "1VayNert3x1KzbpzMGt2qdqrAThiRov55",
            "vchange_value": 97907074
        }]
    }


@pytest.fixture
def unified_block_for_dict_compare() -> UnifiedBlock:
    return UnifiedBlock()


def test_calc_block_merkle_root(unified_block):
    txids_concat = "66b59b129bca8162813b8933fe5b29dc2d6631a67c64dcbc37291815806095a1" +  \
        "79424b88393c8ae9d773d7cf96a1bd17f225b2feba00cb8d7de29b06d0f79893"
    txids_concat_encoded = str.encode(txids_concat)
    sha256_hash = sha256()
    sha256_hash.update(txids_concat_encoded)

    txids_concat_sha = sha256_hash.hexdigest()

    assert unified_block.merkle_root == txids_concat_sha


def test_init_unified_block_from_dict(unified_block_dict: Dict, unified_block: UnifiedBlock):
    print(unified_block_dict['timestamp'])
    print(unified_block.timestamp)