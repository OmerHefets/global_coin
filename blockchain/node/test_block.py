import pytest
from datetime import datetime
from exceptions import BlockException
from block import Block


@pytest.fixture
def test_block():
    return Block(hash="00000000000000027e7ba6fe7bad39faf3b5a83daed765f05f7d1b71a1632249",
                 prev_block_hash="00000000000000027e7ba6fe7bad39faf3b5a83daed765f05f7d173951632249",
                 merkle_root="5e049f4030e0ab2debb92378f53c0a6e09548aea083f3ab25e1d94ea1155e29d",
                 timestamp=datetime.timestamp(datetime(year=2022, month=11, day=26)),
                 difficulty=180923195.25802612,
                 nonce=4215469401,
                 height=124193)


@pytest.mark.parametrize(argnames="new_hash",
                         argvalues=[("343525"),
                                    ("abc483293"),
                                    ("blabla"),
                                    ])
def test_set_valid_hash(test_block, new_hash):
    test_block.hash = new_hash
    assert test_block.hash == new_hash


@pytest.mark.parametrize(argnames="new_hash",
                         argvalues=[(12345),
                                    (1.323), 
                                    ([1, 2, 3]), 
                                    ({"hash": 34555}),
                                    ("2")
                                    ])
def test_set_invalid_hash(test_block, new_hash):
    with pytest.raises(BlockException):
        test_block.hash = new_hash

def test_timestamp(test_block):
    print(test_block.timestamp)
