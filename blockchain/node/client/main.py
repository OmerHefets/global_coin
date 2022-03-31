import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi import FastAPI, HTTPException
from routers import blockchain_data_getters, chain_consensus, node_data_getters

bazooka_app = FastAPI()

bazooka_app.include_router(router=blockchain_data_getters.router)
bazooka_app.include_router(router=chain_consensus.router)
bazooka_app.include_router(router=node_data_getters.router)
