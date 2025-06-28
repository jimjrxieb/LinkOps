from fastapi import FastAPI
from routes import logs, agents, orbs_runes, reloop, webscrape

app = FastAPI(title="ScraperDash")

app.include_router(logs.router)
app.include_router(agents.router)
app.include_router(orbs_runes.router)
app.include_router(reloop.router)
app.include_router(webscrape.router)
