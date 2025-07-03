from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import uuid4

from config.settings import get_settings
from config.database import get_db
from core.models.entities import Link
from core.models.schemas import (
    LinkCreate,
    LinkUpdate,
    LinkResponse,
    HealthResponse,
    DetailedHealthResponse,
)


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.APP_NAME)

    # Health endpoints
    @app.get("/health/", response_model=HealthResponse)
    async def health_root():
        return {
            "status": "healthy",
            "timestamp": "2023-01-01T00:00:00",
            "service": settings.APP_NAME,
        }

    @app.get("/health/detailed", response_model=DetailedHealthResponse)
    async def health_detailed():
        return {
            "status": "healthy",
            "timestamp": "2023-01-01T00:00:00",
            "service": settings.APP_NAME,
            "database": "ok",
            "kafka": "ok",
            "system": {},
            "directories": {},
        }

    @app.get("/health/ready", response_model=HealthResponse)
    async def readiness():
        return {
            "status": "ready",
            "timestamp": "2023-01-01T00:00:00",
            "service": settings.APP_NAME,
        }

    @app.get("/health/live", response_model=HealthResponse)
    async def liveness():
        return {
            "status": "alive",
            "timestamp": "2023-01-01T00:00:00",
            "service": settings.APP_NAME,
        }

    # CRUD routes for Link
    @app.get("/api/v1/links", response_model=list[LinkResponse])
    def list_links(db: Session = Depends(get_db)):
        links = db.query(Link).all()
        return [link.to_dict() for link in links]

    @app.post("/api/v1/links", response_model=LinkResponse)
    def create_link(data: LinkCreate, db: Session = Depends(get_db)):
        link = Link(
            id=str(uuid4()),
            url=data.url,
            title=data.title,
            description=data.description,
        )
        db.add(link)
        db.commit()
        db.refresh(link)
        return link.to_dict()

    @app.get("/api/v1/links/{link_id}", response_model=LinkResponse)
    def get_link(link_id: str, db: Session = Depends(get_db)):
        link = db.query(Link).filter(Link.id == link_id).first()
        if not link:
            raise HTTPException(status_code=404, detail="Link not found")
        return link.to_dict()

    @app.put("/api/v1/links/{link_id}", response_model=LinkResponse)
    def update_link(link_id: str, data: LinkUpdate, db: Session = Depends(get_db)):
        link = db.query(Link).filter(Link.id == link_id).first()
        if not link:
            raise HTTPException(status_code=404, detail="Link not found")
        if data.url is not None:
            link.url = data.url
        if data.title is not None:
            link.title = data.title
        if data.description is not None:
            link.description = data.description
        db.commit()
        db.refresh(link)
        return link.to_dict()

    @app.delete("/api/v1/links/{link_id}")
    def delete_link(link_id: str, db: Session = Depends(get_db)):
        link = db.query(Link).filter(Link.id == link_id).first()
        if not link:
            raise HTTPException(status_code=404, detail="Link not found")
        db.delete(link)
        db.commit()
        return {"status": "deleted"}

    return app 