"""
LinkOps Core - Database Models
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
from typing import Dict, Any
import sys

Base = declarative_base()


class Log(Base):
    """Log model for storing sanitized training data"""

    __tablename__ = "logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent = Column(String(100), nullable=False)
    task_id = Column(String(255), nullable=False, index=True)
    action = Column(String(255), nullable=False)
    result = Column(Text, nullable=False)
    sanitized = Column(Boolean, default=True)
    approved = Column(Boolean, default=False)
    auto_approved = Column(Boolean, default=False)
    compliance_tags = Column(Text, default="[]")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Log(id='{self.id}', task_id='{self.task_id}', agent='{self.agent}')>"


class WhisQueue(Base):
    """Whis Queue model for storing tasks that need training"""

    __tablename__ = "whis_queue"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(String(255), nullable=False, index=True)
    raw_text = Column(Text, nullable=False)
    source = Column(String(100), default="data-collection")
    status = Column(
        String(50), default="pending", index=True
    )  # pending, trained, approved
    agent = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return (
            f"<WhisQueue(id='{self.id}', task_id='{self.task_id}', "
            f"source='{self.source}', status='{self.status}')>"
        )
