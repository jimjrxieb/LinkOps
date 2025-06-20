"""
SQLAlchemy models for LinkOps Core
"""

from sqlalchemy import Column, String, Text, Integer, DateTime, UUID, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()


class Orb(Base):
    """Orb model representing a collection of runes"""
    __tablename__ = "orbs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    category = Column(String(100), index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship to runes
    runes = relationship("Rune", back_populates="orb", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Orb(id='{self.id}', name='{self.name}', category='{self.category}')>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class Rune(Base):
    """Rune model representing scripts within an orb"""
    __tablename__ = "runes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    orb_id = Column(UUID(as_uuid=True), ForeignKey("orbs.id"), nullable=False, index=True)
    script_path = Column(String(500), nullable=False)
    language = Column(String(50), nullable=False, index=True)
    version = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship to orb
    orb = relationship("Orb", back_populates="runes")
    
    def __repr__(self):
        return f"<Rune(id='{self.id}', orb_id='{self.orb_id}', language='{self.language}', version={self.version})>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": str(self.id),
            "orb_id": str(self.orb_id),
            "script_path": self.script_path,
            "language": self.language,
            "version": self.version,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Log(Base):
    """Log model for tracking agent actions and results"""
    __tablename__ = "logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent = Column(String(100), nullable=False, index=True)
    task_id = Column(String(100), nullable=False, index=True)
    action = Column(Text, nullable=False)
    result = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Log(id='{self.id}', agent='{self.agent}', task_id='{self.task_id}', action='{self.action[:50]}...')>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": str(self.id),
            "agent": self.agent,
            "task_id": self.task_id,
            "action": self.action,
            "result": self.result,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


# Additional models for LinkOps Core functionality
class Link(Base):
    """Link entity model"""
    __tablename__ = "links"
    
    id = Column(String(36), primary_key=True, index=True)
    url = Column(String(2048), nullable=False, index=True)
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    screenshot_path = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
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
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
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
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
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
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<SystemMetric(id='{self.id}', metric_name='{self.metric_name}', value='{self.metric_value}')>"
