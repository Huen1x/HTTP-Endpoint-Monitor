from fastapi import FastAPI

from models import init_db
from router import router

app = FastAPI(title="Endpoint Cheker")

init_db()

app.include_router(router, prefix="/endpoints", tags=["endpoints"])
