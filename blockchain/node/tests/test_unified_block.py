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

def test_calc_block_merkle_root(unified_block):
    txids_concat = "bbf9516f9e14ce192b299505d6e5ba44c2dc1158a0e1790cbfddd3208d40353c" +  \
        "4a5c1a769ac65e2ec25dc0ef68db339e80b623ed71009df9689fb41201957e07"
    txids_concat_encoded = str.encode(txids_concat)
    sha256_hash = sha256()
    sha256_hash.update(txids_concat_encoded)

    txids_concat_sha = sha256_hash.hexdigest()

    assert unified_block.merkle_root == txids_concat_sha