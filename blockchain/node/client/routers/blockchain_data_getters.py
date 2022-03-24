from fastapi import APIRouter

router = APIRouter()

@router.get("/blockchain/block_hash/{hash}", response_model="", status_code=101)
def pass_1():
    pass


@router.get("/blockchain/block_height/{height}", response_model="", status_code=101)
def pass_2():
    pass


@router.get("/blockchain/latest", response_model="", status_code=101)
def pass_3():
    pass


@router.get("/transaction/txid/{txid}", response_model="", status_code=101)
def pass_4():
    pass


@router.get("/transaction/block_hash/{hash}", response_model="", status_code=101)
def pass_5():
    pass


@router.get("/tx_pool/txid/{txid}", response_model="", status_code=101)
def pass_6():
    pass


@router.get("/tx_pool/top_100", response_model="", status_code=101)
def pass_7():
    pass
