"""
Shared Task Schemas
Pydantic schemas for task operations across LinkOps microservices
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    """Task status enumeration"""

    PENDING = "pending"
    EVALUATING = "evaluating"
    APPROVED = "approved"
    REJECTED = "rejected"
    DEPLOYING = "deploying"
    DEPLOYED = "deployed"
    FAILED = "failed"
    COMPLETED = "completed"


class TaskPriority(str, Enum):
    """Task priority enumeration"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskType(str, Enum):
    """Task type enumeration"""

    INFRASTRUCTURE = "infrastructure"
    KUBERNETES = "kubernetes"
    ASSISTANT = "assistant"
    ML_TRAINING = "ml_training"
    SECURITY = "security"
    PLATFORM = "platform"
    VOICE = "voice"
    IMAGE = "image"
    ENHANCEMENT = "enhancement"
    DEPLOYMENT = "deployment"
    SCALING = "scaling"
    ANALYSIS = "analysis"


class TaskBase(BaseModel):
    """Base task schema"""

    title: str = Field(..., description="Task title")
    task_type: TaskType = Field(..., description="Type of task")
    description: Optional[str] = Field(None, description="Task description")
    requirements: Optional[List[str]] = Field(
        default_factory=list, description="Task requirements"
    )
    parameters: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Task parameters"
    )


class TaskCreate(TaskBase):
    """Schema for creating a task"""

    task_id: Optional[str] = Field(None, description="Custom task ID")
    task_priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM, description="Task priority"
    )
    submitted_by: str = Field(..., description="Who submitted the task")
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Additional metadata"
    )


class TaskUpdate(BaseModel):
    """Schema for updating a task"""

    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[List[str]] = None
    parameters: Optional[Dict[str, Any]] = None
    task_priority: Optional[TaskPriority] = None
    metadata: Optional[Dict[str, Any]] = None


class TaskEvaluation(BaseModel):
    """Schema for task evaluation result"""

    logic_source: str = Field(..., description="Recommended logic source")
    score: int = Field(..., ge=0, le=100, description="Evaluation score")
    confidence: str = Field(..., description="Confidence level")
    reason: str = Field(..., description="Evaluation reason")
    recommendation: Dict[str, Any] = Field(..., description="Full recommendation")


class TaskResponse(TaskBase):
    """Schema for task response"""

    id: int
    task_id: str
    task_priority: TaskPriority
    status: TaskStatus
    assigned_logic_source: Optional[str] = None
    assigned_agent: Optional[str] = None
    evaluation_score: Optional[int] = None
    evaluation_result: Optional[Dict[str, Any]] = None
    submitted_by: str
    submitted_at: datetime
    evaluated_at: Optional[datetime] = None
    deployed_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any]

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Schema for task list response"""

    tasks: List[TaskResponse]
    total_count: int
    page: int
    page_size: int


class TaskFilter(BaseModel):
    """Schema for filtering tasks"""

    task_type: Optional[TaskType] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assigned_logic_source: Optional[str] = None
    assigned_agent: Optional[str] = None
    submitted_by: Optional[str] = None
    search: Optional[str] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
