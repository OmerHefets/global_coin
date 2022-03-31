import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi import APIRouter, status
from client.routers.chain_consensus import DIFFICULTY

router = APIRouter()

@router.get("/node/difficulty", status_code=status.HTTP_200_OK)
def get_difficulty():
    return {"difficulty": DIFFICULTY}
