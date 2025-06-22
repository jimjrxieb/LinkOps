"""
SQLAlchemy models for LinkOps Core
"""

from sqlalchemy import Column, String, Text, Integer, DateTime, UUID, ForeignKey, func, Boolean, Float
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
    owner_agent = Column(String(50), index=True)  # "katie", "igris", "whis", "james"
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship to runes
    runes = relationship("Rune", back_populates="orb", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Orb(id='{self.id}', name='{self.name}', category='{self.category}', owner_agent='{self.owner_agent}')>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "owner_agent": self.owner_agent,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class Rune(Base):
    """Rune model representing scripts within an orb"""
    __tablename__ = "runes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    orb_id = Column(UUID(as_uuid=True), ForeignKey("orbs.id"), nullable=False, index=True)
    script_path = Column(String(500), nullable=True)  # Made nullable since we'll use script_content
    script_content = Column(Text, nullable=True)  # Store actual script content
    language = Column(String(50), nullable=False, index=True)
    version = Column(Integer, default=1, nullable=False)
    task_id = Column(String(255), nullable=True, index=True)  # Task identifier
    owner_agent = Column(String(50), index=True)  # "katie", "igris", "whis", "james"
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Feedback fields
    feedback_score = Column(Float, default=0.0)
    feedback_count = Column(Integer, default=0)
    last_feedback = Column(Text)
    is_flagged = Column(Boolean, default=False)
    
    # Relationship to orb
    orb = relationship("Orb", back_populates="runes")
    
    def __repr__(self):
        return f"<Rune(id='{self.id}', orb_id='{self.orb_id}', language='{self.language}', version={self.version}, owner_agent='{self.owner_agent}')>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": str(self.id),
            "orb_id": str(self.orb_id),
            "script_path": self.script_path,
            "script_content": self.script_content,
            "language": self.language,
            "version": self.version,
            "task_id": self.task_id,
            "owner_agent": self.owner_agent,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "feedback_score": self.feedback_score,
            "feedback_count": self.feedback_count,
            "last_feedback": self.last_feedback,
            "is_flagged": self.is_flagged
        }


class WhisQueue(Base):
    """Whis Queue model for storing tasks that need training"""
    __tablename__ = "whis_queue"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(String(255), nullable=False, index=True)
    raw_text = Column(Text, nullable=False)
    source = Column(String(100), default="james")  # e.g., "openai_fallback", "exam_data"
    status = Column(String(50), default="pending", index=True)  # pending, trained, approved
    agent = Column(String(100))  # NEW: katie, igris, whis, james
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<WhisQueue(id='{self.id}', task_id='{self.task_id}', source='{self.source}', status='{self.status}')>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": str(self.id),
            "task_id": self.task_id,
            "raw_text": self.raw_text,
            "source": self.source,
            "status": self.status,
            "agent": self.agent,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Approval(Base):
    """Approval model for Whis suggestions"""
    __tablename__ = "approvals"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    suggestion = Column(Text, nullable=False)
    approved = Column(Boolean, default=False)
    reviewed_at = Column(DateTime, default=None, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Approval(id='{self.id}', approved={self.approved})>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": str(self.id),
            "suggestion": self.suggestion,
            "approved": self.approved,
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None,
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


class Task(Base):
    __tablename__ = "tasks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    input_text = Column(Text, nullable=False)
    agent_rankings = Column(Text)  # Store as JSON string like {"katie": 92, "igris": 15, "whis": 5}
    assigned_to = Column(String, nullable=True)
    resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Additional fields for task management
    status = Column(String(50), default="pending", index=True)  # pending, assigned, resolved, failed
    origin = Column(String(50), default="manual")  # manual, manager, agent
    priority = Column(String(20), default="medium")  # high, medium, low
    tags = Column(Text)  # JSON array of tags
    assigned_agent = Column(String(50), nullable=True, index=True)
    assigned_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    result = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<Task(id='{self.id}', input_text='{self.input_text[:50]}...', status='{self.status}')>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": str(self.id),
            "input_text": self.input_text,
            "agent_rankings": self.agent_rankings,
            "assigned_to": self.assigned_to,
            "resolved": self.resolved,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "status": self.status,
            "origin": self.origin,
            "priority": self.priority,
            "tags": self.tags,
            "assigned_agent": self.assigned_agent,
            "assigned_at": self.assigned_at.isoformat() if self.assigned_at else None,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "result": self.result
        }


class AgentTask(Base):
    """Agent Task model for tracking agent task assignments and execution"""
    __tablename__ = "agent_tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False, index=True)
    agent_id = Column(String(50), nullable=False, index=True)  # katie, igris, whis
    status = Column(String(50), default="pending", index=True)  # pending, running, completed, failed
    priority = Column(String(20), default="medium")  # high, medium, low
    complexity_score = Column(Float, default=0.5)  # 0.0 to 1.0
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    result = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<AgentTask(id='{self.id}', task_id='{self.task_id}', agent_id='{self.agent_id}', status='{self.status}')>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": str(self.id),
            "task_id": str(self.task_id),
            "agent_id": self.agent_id,
            "status": self.status,
            "priority": self.priority,
            "complexity_score": self.complexity_score,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": self.result,
            "error_message": self.error_message
        }
