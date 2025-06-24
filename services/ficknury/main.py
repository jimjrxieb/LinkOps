from fastapi import FastAPI
from routes import evaluate, deploy, verify, creds

app = FastAPI(title="FickNury Agent Commander")

app.include_router(evaluate.router)
app.include_router(deploy.router)
app.include_router(verify.router)
app.include_router(creds.router) 