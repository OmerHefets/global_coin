import pytest
from datetime import datetime, timedelta
from exceptions import BlockException
from block import Block


@pytest.fixture
def test_block() -> Block:
    return Block(hash="00000000000000027e7ba6fe7bad39faf3b5a83daed765f05f7d1b71a1632249",
                 prev_block_hash="00000000000000027e7ba6fe7bad39faf3b5a83daed765f05f7d173951632249",
                 merkle_root="5e049f4030e0ab2debb92378f53c0a6e09548aea083f3ab25e1d94ea1155e29d",
                 timestamp=datetime.timestamp(
                     datetime(year=2021, month=11, day=26)),
                 difficulty=180923195.25802612,
                 nonce=4215469401,
                 height=124193)


@pytest.mark.parametrize(argnames="new_hash",
                         argvalues=[("00000000000000027e7ba6fe7bad39faf3b5a83daed765f05f7d1b71a1632255"),
                                    ("00000000000000027E7BA6FE7BAD39FAF3B5A83DAED765F05F7D1B71A1632249"),
                                    ("00000000000000027E7BA6fe7bad39fAf3B5a83DAed765f05f7d1b71a1632249"),
                                    ])
def test_set_valid_hash(test_block, new_hash):
    """
    A valid hash is in the format of: 64 characters, HEXA only, string only

    """
    test_block.hash = new_hash
    assert test_block.hash == new_hash


@pytest.mark.parametrize(argnames="new_hash",
                         argvalues=[(12345),
                                    (1.323),
                                    ([1, 2, 3]),
                                    ({"hash": 34555}),
                                    ("000027E7BA6fe7bad39fAf3B5a83DAed765f05f7d1b71a1632249")
                                    ])
def test_set_invalid_hash(test_block, new_hash):
    with pytest.raises(BlockException):
        test_block.hash = new_hash


@pytest.mark.parametrize(argnames="new_timestamp",
                         argvalues=[(datetime.timestamp(datetime.now())),
                                    (datetime.timestamp(
                                        datetime.now() - timedelta(minutes=5))),
                                    (datetime.timestamp(
                                        datetime.now() + timedelta(seconds=30)))
                                    ])
def test_set_valid_timestamp(test_block, new_timestamp):
    test_block.timestamp = new_timestamp
    assert test_block.timestamp == new_timestamp


@pytest.mark.parametrize(argnames="new_timestamp",
                         argvalues=[(datetime(year=2021, month=10, day=10)),
                                    (datetime.timestamp(datetime.now() + timedelta(minutes=2))),
                                    (str(datetime.timestamp(datetime.now())))
                                    ])
def test_set_invalid_timestamp(test_block, new_timestamp):
    with pytest.raises(BlockException):
        test_block.timestamp = new_timestamp
