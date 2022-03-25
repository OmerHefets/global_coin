from typing import Optional
from pydantic import BaseModel

class BlockModel(BaseModel):
    hash: str
    prev_block_hash: str
    merkle_root: str
    nonce: int
    height: int
    difficulty: float
    timestamp: float

class TxModel(BaseModel):
    txid: str
    tx_block_hash: str
    tx_block_index: int
    vin: str
    vout_addr: str
    vout_value: int
    vout_script: str
    vchange_addr: str
    vchange_value: int
    vchange_script: str

class TxPoolModel(BaseModel):
    txid: str
    vin: str
    vout_addr: str
    vout_value: int
    vout_script: str
    vchange_addr: str
    vchange_value: int
    vchange_script: str