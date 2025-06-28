from fastapi import FastAPI
from routes import chat, actions, explain

app = FastAPI(title="James – LinkOps Assistant")

app.include_router(chat.router)
app.include_router(actions.router)
app.include_router(explain.router)
