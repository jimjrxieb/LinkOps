"""
Shared Agent Log Model
Database model for agent logs used across LinkOps microservices
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from typing import Optional, Dict, Any
from shared.config.database import Base


class AgentLog(Base):
    """Agent log model for storing agent activity"""

    __tablename__ = "agent_logs"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String(100), nullable=False, index=True)
    logic_source = Column(
        String(100), nullable=True, index=True
    )  # igris_logic, katie_logic, etc.
    log_level = Column(
        String(20), nullable=False, index=True
    )  # INFO, WARNING, ERROR, DEBUG
    message = Column(Text, nullable=False)
    operation = Column(
        String(100), nullable=True, index=True
    )  # task_execution, enhancement, etc.
    task_id = Column(String(100), nullable=True, index=True)
    metadata = Column(JSON, nullable=True)  # Additional log metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<AgentLog(id={self.id}, agent='{self.agent_name}', level='{self.log_level}')>"

    def to_dict(self) -> Dict[str, Any]:
        """Convert log to dictionary"""
        return {
            "id": self.id,
            "agent_name": self.agent_name,
            "logic_source": self.logic_source,
            "log_level": self.log_level,
            "message": self.message,
            "operation": self.operation,
            "task_id": self.task_id,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    @classmethod
    def create_log(
        cls,
        agent_name: str,
        message: str,
        log_level: str = "INFO",
        logic_source: Optional[str] = None,
        operation: Optional[str] = None,
        task_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "AgentLog":
        """Create a new agent log entry"""
        return cls(
            agent_name=agent_name,
            message=message,
            log_level=log_level.upper(),
            logic_source=logic_source,
            operation=operation,
            task_id=task_id,
            metadata=metadata or {},
        )

    @classmethod
    def log_info(cls, agent_name: str, message: str, **kwargs) -> "AgentLog":
        """Create INFO level log"""
        return cls.create_log(agent_name, message, "INFO", **kwargs)

    @classmethod
    def log_warning(cls, agent_name: str, message: str, **kwargs) -> "AgentLog":
        """Create WARNING level log"""
        return cls.create_log(agent_name, message, "WARNING", **kwargs)

    @classmethod
    def log_error(cls, agent_name: str, message: str, **kwargs) -> "AgentLog":
        """Create ERROR level log"""
        return cls.create_log(agent_name, message, "ERROR", **kwargs)

    @classmethod
    def log_debug(cls, agent_name: str, message: str, **kwargs) -> "AgentLog":
        """Create DEBUG level log"""
        return cls.create_log(agent_name, message, "DEBUG", **kwargs)
