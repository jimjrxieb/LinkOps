from fastapi import FastAPI
from routes import clean

app = FastAPI(title="Sanitizer Service")

app.include_router(clean.router)
