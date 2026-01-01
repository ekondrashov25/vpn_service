from fastapi import FastAPI
from backend.api.vpn import router as vpn_router

app = FastAPI(title="vpn")

app.include_router(vpn_router, prefix="/vpn")