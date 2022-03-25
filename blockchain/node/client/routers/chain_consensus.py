import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import Dict
from fastapi import APIRouter, status, HTTPException, Response
from node.client.internal.schemas import BlockModel, TxPoolModel
from node.bl.block_validator import BlockValidator
from node.bl.unified_block import UnifiedBlock
from node.bl.exceptions import BlockValidationException

DIFFICULTY = 13
router = APIRouter()

@router.post("/insert/block", status_code=status.HTTP_201_CREATED)
def insert_new_block(block, response: Response):
    bv = BlockValidator()
    try:
        if bv.validate_block(unified_block=block, req_difficulty=DIFFICULTY):
            # remove tx's from the tx pool
            # remove tx's from the utxo list
            pass
        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": f"Your block is invalid."}
    except BlockValidationException:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": f"Your block is invalid."}


@router.post("/insert/transaction", status_code=status.HTTP_201_CREATED)
def pass_2():
    pass
