import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import Dict
from fastapi import APIRouter, status, HTTPException, Response
from node.client.internal.schemas import BlockModel, TxPoolModel, UnifiedBlockModel
from node.bl.block_validator import BlockValidator
from node.bl.unified_block import UnifiedBlock
from node.bl.exceptions import BlockValidationException
from client.routers.blockchain_data_getters import bazooka_cli

DIFFICULTY = 21
router = APIRouter()

@router.post("/insert/block", status_code=status.HTTP_201_CREATED)
def insert_new_block(block: UnifiedBlockModel, response: Response):
    bv = BlockValidator()
    unified_block = UnifiedBlock.init_unified_block_from_dict(dict(block))
    try:
        if bv.validate_block(unified_block=unified_block, req_difficulty=DIFFICULTY):
            # insert the block
            bazooka_cli.insert_new_unified_block(unified_block=unified_block)
            # remove tx's from the tx pool
            bazooka_cli.remove_txs_in_block_from_tx_pool(unified_block=unified_block)
            # remove tx's from the utxo list
            bazooka_cli.remove_txs_in_block_from_utxo(unified_block=unified_block)
            # update new utxos
            bazooka_cli.update_new_utxos(unified_block=unified_block)

            return {"detail": f"Block number {unified_block.height} was created succesfully."}
        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": f"Your block is invalid."}
    except BlockValidationException:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": f"Your block is invalid."}


@router.post("/insert/transaction", status_code=status.HTTP_201_CREATED)
def insert_new_transaction():
    pass
