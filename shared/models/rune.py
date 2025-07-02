"""
Shared Rune Model
Database model for Runes used across LinkOps microservices
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, Dict, Any

from shared.config.database import Base


class Rune(Base):
    """Rune model for storing Whis-generated runes"""

    __tablename__ = "runes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    rune_type = Column(
        String(100), nullable=False, index=True
    )  # training, enhancement, etc.
    status = Column(
        String(50), default="pending", index=True
    )  # pending, active, deprecated
    metadata = Column(JSON, nullable=True)  # Additional rune metadata
    created_by = Column(String(100), nullable=False)  # Which agent created it
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True, index=True)

    # Relationships
    training_logs = relationship("TrainingLog", back_populates="rune")

    def __repr__(self):
        return f"<Rune(id={self.id}, name='{self.name}', type='{self.rune_type}')>"

    def to_dict(self) -> Dict[str, Any]:
        """Convert rune to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "content": self.content,
            "rune_type": self.rune_type,
            "status": self.status,
            "metadata": self.metadata,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_active": self.is_active,
        }

    @classmethod
    def create_rune(
        cls,
        name: str,
        content: str,
        rune_type: str,
        created_by: str,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "Rune":
        """Create a new rune"""
        return cls(
            name=name,
            content=content,
            rune_type=rune_type,
            created_by=created_by,
            description=description,
            metadata=metadata or {},
        )

    def activate(self):
        """Activate the rune"""
        self.status = "active"
        self.is_active = True

    def deactivate(self):
        """Deactivate the rune"""
        self.status = "deprecated"
        self.is_active = False

    def update_content(self, new_content: str, description: Optional[str] = None):
        """Update rune content"""
        self.content = new_content
        if description:
            self.description = description
        self.updated_at = datetime.utcnow()
