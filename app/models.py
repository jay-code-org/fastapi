
from sqlalchemy import TIMESTAMP, UUID, Column, ForeignKey, String, text, LargeBinary
from sqlalchemy.orm import relationship
from .database import Base

""" Status Model"""


class Status(Base):
    __tablename__ = "statuses"
    id = Column(UUID, primary_key=True,
                server_default=text("gen_random_uuid()"), nullable=False)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text("now()"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)


""" Category Model"""


class Category(Base):
    __tablename__ = "categories"
    id = Column(UUID, primary_key=True,
                server_default=text("gen_random_uuid()"), nullable=False)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text("now()"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)


""" Role Model"""


class Role(Base):
    __tablename__ = "roles"
    id = Column(UUID, primary_key=True,
                server_default=text("gen_random_uuid()"), nullable=False)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text("now()"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)


""" ToDo Model """


class Todo(Base):
    __tablename__ = "todos"
    id = Column(UUID, primary_key=True,
                server_default=text("gen_random_uuid()"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category_id = Column(UUID, ForeignKey(
        "categories.id"), nullable=False)
    category = relationship("Category")
    status_id = Column(UUID, ForeignKey("statuses.id"), nullable=False)
    status = relationship("Status")
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text("now()"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)
    owner_id = Column(UUID, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")


""" User Model """


class User(Base):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True, server_default=text(
        "gen_random_uuid()"), nullable=False)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(LargeBinary, nullable=False)
    status_id = Column(UUID, ForeignKey("statuses.id"), nullable=False)
    role_id = Column(UUID, ForeignKey("roles.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text("now()"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)
