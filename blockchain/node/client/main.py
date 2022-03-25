import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi import FastAPI, HTTPException
from routers import blockchain_data_getters, validators

bazooka_app = FastAPI()

bazooka_app.include_router(router=blockchain_data_getters.router)
bazooka_app.include_router(router=validators.router)
