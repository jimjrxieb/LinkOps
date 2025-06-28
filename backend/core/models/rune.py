from sqlalchemy import Column, Integer, String, JSON, Boolean, DateTime, func
from config.database import Base

class RuneCandidate(Base):
    __tablename__ = "runes_pending"

    id = Column(Integer, primary_key=True, index=True)
    agent = Column(String, index=True)
    origin = Column(String)
    content = Column(JSON)
    approved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 