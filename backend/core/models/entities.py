"""
SQLAlchemy database models/entities
"""

from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func
from datetime import datetime

from config.database import Base


class Link(Base):
    """Link entity model"""

    __tablename__ = "links"

    id = Column(String(36), primary_key=True, index=True)
    url = Column(String(2048), nullable=False, index=True)
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    screenshot_path = Column(String(500), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    def __repr__(self):
        return f"<Link(id='{self.id}', url='{self.url}', title='{self.title}')>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "url": self.url,
            "title": self.title,
            "description": self.description,
            "screenshot_path": self.screenshot_path,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class AuditLog(Base):
    """Audit log entity for tracking changes"""

    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, index=True)
    entity_type = Column(String(50), nullable=False, index=True)
    entity_id = Column(String(36), nullable=False, index=True)
    action = Column(String(20), nullable=False)  # CREATE, UPDATE, DELETE
    changes = Column(Text, nullable=True)  # JSON string of changes
    user_id = Column(String(36), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self):
        return f"<AuditLog(id='{self.id}', entity_type='{self.entity_type}', action='{self.action}')>"


class SystemMetric(Base):
    """System metrics entity for monitoring"""

    __tablename__ = "system_metrics"

    id = Column(String(36), primary_key=True, index=True)
    metric_name = Column(String(100), nullable=False, index=True)
    metric_value = Column(String(255), nullable=False)
    metric_unit = Column(String(20), nullable=True)
    tags = Column(Text, nullable=True)  # JSON string of tags
    timestamp = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self):
        return f"<SystemMetric(id='{self.id}', metric_name='{self.metric_name}', value='{self.metric_value}')>"
