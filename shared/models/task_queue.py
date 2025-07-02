"""
Shared Task Queue Model
Database model for task queue management across LinkOps microservices
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Enum
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, Dict, Any
import enum
from shared.config.database import Base


class TaskStatus(enum.Enum):
    """Task status enumeration"""

    PENDING = "pending"
    EVALUATING = "evaluating"
    APPROVED = "approved"
    REJECTED = "rejected"
    DEPLOYING = "deploying"
    DEPLOYED = "deployed"
    FAILED = "failed"
    COMPLETED = "completed"


class TaskPriority(enum.Enum):
    """Task priority enumeration"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskQueue(Base):
    """Task queue model for managing task processing"""

    __tablename__ = "task_queue"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(100), unique=True, nullable=False, index=True)
    task_type = Column(String(100), nullable=False, index=True)
    task_priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM, index=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, index=True)

    # Task details
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    requirements = Column(JSON, nullable=True)  # List of requirements
    parameters = Column(JSON, nullable=True)  # Task parameters

    # Assignment
    assigned_logic_source = Column(String(100), nullable=True, index=True)
    assigned_agent = Column(String(100), nullable=True, index=True)

    # Scoring
    evaluation_score = Column(Integer, nullable=True)  # 0-100
    evaluation_result = Column(JSON, nullable=True)  # Full evaluation details

    # Processing
    submitted_by = Column(String(100), nullable=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    evaluated_at = Column(DateTime(timezone=True), nullable=True)
    deployed_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Metadata
    metadata = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<TaskQueue(id={self.id}, task_id='{self.task_id}', status='{self.status.value}')>"

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary"""
        return {
            "id": self.id,
            "task_id": self.task_id,
            "task_type": self.task_type,
            "task_priority": self.task_priority.value if self.task_priority else None,
            "status": self.status.value if self.status else None,
            "title": self.title,
            "description": self.description,
            "requirements": self.requirements,
            "parameters": self.parameters,
            "assigned_logic_source": self.assigned_logic_source,
            "assigned_agent": self.assigned_agent,
            "evaluation_score": self.evaluation_score,
            "evaluation_result": self.evaluation_result,
            "submitted_by": self.submitted_by,
            "submitted_at": (
                self.submitted_at.isoformat() if self.submitted_at else None
            ),
            "evaluated_at": (
                self.evaluated_at.isoformat() if self.evaluated_at else None
            ),
            "deployed_at": self.deployed_at.isoformat() if self.deployed_at else None,
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
            "metadata": self.metadata,
        }

    @classmethod
    def create_task(
        cls,
        task_id: str,
        title: str,
        task_type: str,
        submitted_by: str,
        description: Optional[str] = None,
        requirements: Optional[list] = None,
        parameters: Optional[Dict[str, Any]] = None,
        priority: TaskPriority = TaskPriority.MEDIUM,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "TaskQueue":
        """Create a new task"""
        return cls(
            task_id=task_id,
            title=title,
            task_type=task_type,
            submitted_by=submitted_by,
            description=description,
            requirements=requirements or [],
            parameters=parameters or {},
            task_priority=priority,
            metadata=metadata or {},
        )

    def update_status(self, status: TaskStatus, **kwargs):
        """Update task status and related timestamps"""
        self.status = status

        if status == TaskStatus.EVALUATING:
            self.evaluated_at = datetime.utcnow()
        elif status == TaskStatus.DEPLOYED:
            self.deployed_at = datetime.utcnow()
        elif status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
            self.completed_at = datetime.utcnow()

        # Update any additional fields
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def assign_to_logic_source(self, logic_source: str):
        """Assign task to a logic source"""
        self.assigned_logic_source = logic_source
        self.status = TaskStatus.APPROVED

    def assign_to_agent(self, agent_name: str):
        """Assign task to a deployed agent"""
        self.assigned_agent = agent_name
        self.status = TaskStatus.DEPLOYING

    def set_evaluation_result(self, score: int, result: Dict[str, Any]):
        """Set evaluation result and score"""
        self.evaluation_score = score
        self.evaluation_result = result
        self.evaluated_at = datetime.utcnow()

        # Auto-assign if score is high enough
        if score >= 80 and result.get("recommendation", {}).get("action") == "approve":
            logic_source = result.get("best_logic_source", {}).get("logic_source")
            if logic_source:
                self.assign_to_logic_source(logic_source)
