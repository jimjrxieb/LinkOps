from fastapi import FastAPI
from routes import train, approvals, digest

app = FastAPI(title="Whis AI Agent")

app.include_router(train.router)
app.include_router(approvals.router)
app.include_router(digest.router) 