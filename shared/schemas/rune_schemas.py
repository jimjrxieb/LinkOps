"""
Shared Rune Schemas
Pydantic schemas for Rune operations across LinkOps microservices
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class RuneType(str, Enum):
    """Rune type enumeration"""
    TRAINING = "training"
    ENHANCEMENT = "enhancement"
    DEPLOYMENT = "deployment"
    ANALYSIS = "analysis"
    SECURITY = "security"

class RuneStatus(str, Enum):
    """Rune status enumeration"""
    PENDING = "pending"
    ACTIVE = "active"
    DEPRECATED = "deprecated"

class RuneBase(BaseModel):
    """Base rune schema"""
    name: str = Field(..., description="Rune name")
    description: Optional[str] = Field(None, description="Rune description")
    content: str = Field(..., description="Rune content")
    rune_type: RuneType = Field(..., description="Type of rune")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")

class RuneCreate(RuneBase):
    """Schema for creating a rune"""
    created_by: str = Field(..., description="Agent that created the rune")

class RuneUpdate(BaseModel):
    """Schema for updating a rune"""
    name: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    rune_type: Optional[RuneType] = None
    status: Optional[RuneStatus] = None
    metadata: Optional[Dict[str, Any]] = None

class RuneResponse(RuneBase):
    """Schema for rune response"""
    id: int
    status: RuneStatus
    created_by: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_active: bool
    
    class Config:
        from_attributes = True

class RuneListResponse(BaseModel):
    """Schema for rune list response"""
    runes: List[RuneResponse]
    total_count: int
    page: int
    page_size: int

class RuneFilter(BaseModel):
    """Schema for filtering runes"""
    rune_type: Optional[RuneType] = None
    status: Optional[RuneStatus] = None
    created_by: Optional[str] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100) 