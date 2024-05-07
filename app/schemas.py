from datetime import datetime
from typing import Union
from pydantic import BaseModel, EmailStr
from uuid import UUID
from enum import Enum


# User schemas

class UserBase(BaseModel):
    full_name: str
    phone: Union[str, None] = None


class CreateUser(UserBase):
    email: EmailStr
    password: str


class UpdateUser(UserBase):
    is_active: bool


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(UserBase):
    id: UUID
    email: EmailStr
    created_at: datetime
    updated_at: Union[datetime, None] = None
    is_active: bool = False

    class Config:
        form_attributes = True


# Todo schemas


class TodoCategoryEnum(Enum):
    Sports = "Sports"
    Coding = "Coding"
    Coking = "Cooking"


class TodoStatusEnum(Enum):
    Pending = "Pending"
    Completed = "Completed"
    Deleted = "Deleted"


class TodoBase(BaseModel):
    title: str
    description: str


class CreateTodo(TodoBase):
    category: TodoCategoryEnum
    pass


class UpdateTodo(TodoBase):
    pass


class Todo(TodoBase):
    id: UUID
    status: TodoStatusEnum
    created_at: datetime
    updated_at: Union[datetime, None] = None
    owner_id: UUID
    owner: User

    class Config:
        form_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: str
    id: str
