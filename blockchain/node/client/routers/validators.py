from fastapi import APIRouter

router = APIRouter()

@router.post("/validate/block", response_model="", status_code=101)
def pass_1():
    pass


@router.post("/validate/transaction", response_model="", status_code=101)
def pass_2():
    pass
