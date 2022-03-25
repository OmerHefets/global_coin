import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import List
from node.client.internal.bazooka_client import BazookaClient
from node.client.internal.schemas import BlockModel, TxModel, TxPoolModel
from fastapi import APIRouter, status, HTTPException

bazooka_cli = BazookaClient()


router = APIRouter()

@router.get("/blockchain/block_hash/{hash}", response_model=BlockModel ,status_code=status.HTTP_200_OK)
def get_block_by_hash(hash: str):
    (status_code, block) = bazooka_cli.blockchain_manager.get_block_by_hash(hash=hash)

    if status_code == status.HTTP_404_NOT_FOUND:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Block with hash {hash} does not exist.")

    return block


@router.get("/blockchain/block_height/{height}", response_model=BlockModel, status_code=status.HTTP_200_OK)
def get_block_by_height(height: int):
    (status_code, block) = bazooka_cli.blockchain_manager.get_block_by_height(height=height)

    if status_code == status.HTTP_404_NOT_FOUND:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Block with height {height} does not exist.")

    return block


@router.get("/blockchain/latest", response_model=BlockModel, status_code=status.HTTP_200_OK)
def get_latest_block():
    (status_code, block) = bazooka_cli.blockchain_manager.get_latest_block()

    if status_code == status.HTTP_404_NOT_FOUND:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blockchain is empty. No blocks found.")

    return block


@router.get("/transaction/txid/{txid}", response_model=TxModel, status_code=status.HTTP_200_OK)
def get_tx_by_txid(txid: str):
    (status_code, tx) = bazooka_cli.tx_manager.get_tx_by_txid(txid=txid)

    if status_code == status.HTTP_404_NOT_FOUND:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No tx exists with txid of {txid}.")

    return tx


@router.get("/transaction/block_hash/{block_hash}", response_model=List[TxModel], status_code=status.HTTP_200_OK)
def get_all_txs_in_block(block_hash: str):
    (status_code, tx_list) = bazooka_cli.tx_manager.get_txs_by_block_hash(block_hash=block_hash)

    if status_code == status.HTTP_404_NOT_FOUND:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Block with hash {block_hash} does not exist.")

    return tx_list


@router.get("/tx_pool/txid/{txid}", response_model=TxPoolModel, status_code=status.HTTP_200_OK)
def get_tx_from_pool_by_txid(txid: str):
    (status_code, tx) = bazooka_cli.tx_pool_manager.get_tx_by_txid(txid=txid)

    if status_code == status.HTTP_404_NOT_FOUND:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Tx with hash {txid} does not exist in the tx pool.")

    return tx


@router.get("/tx_pool/top_100", response_model=List[TxPoolModel], status_code=status.HTTP_200_OK)
def get_top_100_txs_in_pool():
    # does not need to save the status code, will return 200 even if empty
    _, tx = bazooka_cli.tx_pool_manager.get_top_100_txs() 

    return tx

