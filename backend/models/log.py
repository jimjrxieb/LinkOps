from sqlalchemy import Column, Integer, String, JSON, DateTime, func
from backend.config.database import Base

class LogEntry(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    input_type = Column(String, index=True)
    source = Column(String, index=True)
    sanitized = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 