"""
Role Model
"""
from datetime import datetime
import uuid

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

from app.db.base import Base


class Role(Base):
    __tablename__ = "ms_role"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("User", back_populates="role")

