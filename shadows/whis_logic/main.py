from fastapi import FastAPI
from routes import train, approvals, digest, ml_operations

app = FastAPI(title="Whis AI Agent - Central ML Brain")

app.include_router(train.router)
app.include_router(approvals.router)
app.include_router(digest.router)
app.include_router(ml_operations.router)
