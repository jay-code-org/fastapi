
from sqlalchemy import TIMESTAMP, UUID, Boolean, Column, Enum, ForeignKey, String, text, LargeBinary
from sqlalchemy.orm import relationship
from .database import Base
from . import schemas

# Todo model


class Todo(Base):
    __tablename__ = "todos"
    id = Column(UUID, primary_key=True,
                server_default=text("gen_random_uuid()"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category = Column(Enum(schemas.TodoCategoryEnum), nullable=False)
    status = Column(Enum(schemas.TodoStatusEnum),
                    default=schemas.TodoStatusEnum.Pending, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text("now()"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)
    owner_id = Column(UUID, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")

# User model


class User(Base):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True, server_default=text(
        "gen_random_uuid()"), nullable=False)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(LargeBinary, nullable=False)
    is_active = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text("now()"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)
