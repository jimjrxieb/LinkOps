from fastapi import APIRouter
from logic.site_crawler import scrape_sources

router = APIRouter(prefix="/api/scraper", tags=["WebScraper"])

@router.post("/external")
def fetch_external():
    results = scrape_sources()
    return {"sources": results}

@router.get("/external")
def get_external_sources():
    results = scrape_sources()
    return {"sources": results} 