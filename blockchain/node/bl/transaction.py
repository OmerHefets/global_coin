import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from hashlib import sha256
from typing import List, Dict
from functools import reduce

HASH_LENGTH = 64  # hash is 32 bytes from SHA-256 hash function

class Transaction:
    def __init__(self,
                 tx_block_hash: str,
                 tx_block_index: int,
                 vin: List[Dict],
                 vout_addr: str,
                 vout_value: int,
                 vout_script: str,
                 vchange_addr: str,
                 vchange_value: int,
                 vchange_script: str) -> None:
        self.tx_block_hash = tx_block_hash
        self.tx_block_index = tx_block_index
        self.vin = vin
        self.vout_addr = vout_addr
        self.vout_value = vout_value
        self.vout_script = vout_script
        self.vchange_addr = vchange_addr
        self.vchange_value = vchange_value
        self.vchange_script = vchange_script
        self.txid = self.calculate_txid_hash()

    def __repr__(self) -> str:
        return f"""Transaction(txid={self.txid},
        tx_block_hash={self.tx_block_hash},
        tx_block_index={self.tx_block_index},
        vin={self.vin},
        vout_addr={self.vout_addr},
        vout_value={self.vout_value},
        vout_script={self.vout_script},
        vchange_addr={self.vchange_value},
        vchange_value={self.vchange_value},
        vchange_script={self.vchange_script})"""

    @property
    def txid(self) -> str:
        return self._txid

    @txid.setter
    def txid(self, new_txid: str) -> None:
        self._txid = new_txid

    @property
    def tx_block_hash(self) -> str:
        return self._tx_block_hash

    @tx_block_hash.setter
    def tx_block_hash(self, new_block_hash: str) -> None:
        self._tx_block_hash = new_block_hash

    @property
    def tx_block_index(self) -> str:
        return self._tx_block_index

    @tx_block_index.setter
    def tx_block_index(self, new_tx_block_index: int) -> None:
        self._tx_block_index = new_tx_block_index

    @property
    def vin(self) -> List[Dict]:
        return self._vin

    @vin.setter
    def vin(self, new_vin: List[Dict]) -> None:
        self._vin = new_vin

    @property
    def vout_addr(self) -> str:
        return self._vout_addr

    @vout_addr.setter
    def vout_addr(self, new_vout_addr) -> None:
        self._vout_addr = new_vout_addr

    @property
    def vout_value(self) -> int:
        return self._vout_value

    @vout_value.setter
    def vout_value(self, new_vout_value) -> None:
        self.vout_value = new_vout_value

    @property
    def vout_script(self) -> str:
        return self._vout_script

    @vout_script.setter
    def vout_script(self, new_vout_script) -> None:
        self._vout_script = new_vout_script

    @property
    def vchange_addr(self) -> str:
        return self._vchange_addr

    @vchange_addr.setter
    def vchange_addr(self, new_vchange_addr) -> None:
        self._vchange_addr = new_vchange_addr

    @property
    def vchange_value(self) -> int:
        return self._vchange_value

    @vchange_value.setter
    def vchange_value(self, new_vchange_value) -> None:
        self._vchange_value = new_vchange_value

    @property
    def vchange_script(self) -> str:
        return self._vchange_script

    @vchange_script.setter
    def vchange_script(self, new_vchange_script) -> None:
        self._vchange_script = new_vchange_script

    @staticmethod
    def flatten_vin_values_to_str(vin_list: List[Dict]):
        flatten_list = [reduce(lambda x, y: str(x)+str(y), d.values()) for d in vin_list]
        vin_str = reduce(lambda x, y: x+y, flatten_list)

        return vin_str

    def calculate_txid_hash(self):
        vin_str = self.flatten_vin_values_to_str(self.vin)
        txid_hash_str = str.encode(vin_str + self.vout_addr + self.vout_script + self.vchange_addr + self.vchange_script)

        sha256_hash = sha256()
        sha256_hash.update(txid_hash_str)

        return sha256_hash.hexdigest()


    