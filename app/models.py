from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from .db import Base

supports = Table(
    "supports",
    Base.metadata,
    Column("evidence_id", ForeignKey("evidence.evidence_id"), primary_key=True),
    Column("subcat_id", ForeignKey("outcome.subcat_id"), primary_key=True),
)

class User(Base):
    __tablename__ = "app_user"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_manager = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    created_owners = relationship("Owner", back_populates="created_by_user")


class Owner(Base):
    __tablename__ = "owner"
    owner_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    jobrole = Column(String, nullable=True)
    created_by_user_id = Column(Integer, ForeignKey("app_user.user_id"), nullable=True)

    evidence_items = relationship("Evidence", back_populates="owner")
    created_by_user = relationship("User", back_populates="created_owners")


class Outcome(Base):
    __tablename__ = "outcome"
    subcat_id = Column(String, primary_key=True, index=True)
    summary = Column(Text, nullable=False)
    category = Column(String, nullable=False)
    function = Column(String, nullable=False)

    evidence_items = relationship("Evidence", secondary=supports, back_populates="outcomes")


class Evidence(Base):
    __tablename__ = "evidence"
    evidence_id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    file_path = Column(String, nullable=False)

    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_reviewed_at = Column(DateTime, default=None, nullable=True)
    lifecycle_length = Column(Integer, default=90, nullable=False)

    owner_id = Column(Integer, ForeignKey("owner.owner_id"), nullable=False)
    owner = relationship("Owner", back_populates="evidence_items")

    outcomes = relationship("Outcome", secondary=supports, back_populates="evidence_items")
    
