from fastapi import FastAPI, HTTPException
from client.routers import blockchain_data_getters, validators


app = FastAPI()

app.include_router(router=blockchain_data_getters.router)
app.include_router(router=validators.router)
