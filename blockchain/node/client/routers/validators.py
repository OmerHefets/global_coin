import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi import APIRouter

router = APIRouter()

@router.post("/validate/block", response_model="", status_code=101)
def pass_1():
    pass


@router.post("/validate/transaction", response_model="", status_code=101)
def pass_2():
    pass
