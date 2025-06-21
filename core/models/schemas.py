"""
Pydantic schemas for API request/response models
"""

from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
from datetime import datetime


class LinkBase(BaseModel):
    """Base link schema"""
    url: HttpUrl = Field(..., description="The URL of the link")
    title: Optional[str] = Field(None, max_length=255, description="Title of the link")
    description: Optional[str] = Field(None, max_length=1000, description="Description of the link")


class LinkCreate(LinkBase):
    """Schema for creating a new link"""
    pass


class LinkUpdate(BaseModel):
    """Schema for updating a link"""
    url: Optional[HttpUrl] = Field(None, description="The URL of the link")
    title: Optional[str] = Field(None, max_length=255, description="Title of the link")
    description: Optional[str] = Field(None, max_length=1000, description="Description of the link")


class LinkResponse(LinkBase):
    """Schema for link response"""
    id: str = Field(..., description="Unique identifier for the link")
    screenshot_path: Optional[str] = Field(None, description="Path to the screenshot file")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    """Schema for health check response"""
    status: str = Field(..., description="Health status")
    timestamp: str = Field(..., description="ISO timestamp")
    service: str = Field(..., description="Service name")


class DetailedHealthResponse(HealthResponse):
    """Schema for detailed health check response"""
    database: str = Field(..., description="Database connection status")
    kafka: str = Field(..., description="Kafka connection status")
    system: dict = Field(..., description="System metrics")
    directories: dict = Field(..., description="Directory status")


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    detail: str = Field(..., description="Error message")
    timestamp: str = Field(..., description="ISO timestamp")
    error_code: Optional[str] = Field(None, description="Error code")


class PaginatedResponse(BaseModel):
    """Schema for paginated responses"""
    items: list = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total number of pages")


class WhisMemoryInput(BaseModel):
    """Schema for Whis memory input"""
    task: str = Field(..., description="The task description")
    solution: str = Field(..., description="The solution or execution steps")
    category: Optional[str] = Field("mlops", description="Category for the task")
    tips: Optional[str] = Field(None, description="Additional tips or best practices")


class WhisMemoryResponse(BaseModel):
    """Schema for Whis memory response"""
    status: str = Field(..., description="Operation status")
    orb_id: str = Field(..., description="ID of the created orb")
    rune_id: Optional[str] = Field(None, description="ID of the created rune")
    task_id: str = Field(..., description="Inferred task ID")
