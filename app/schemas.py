from datetime import datetime
from typing import Union
from pydantic import BaseModel, EmailStr
from uuid import UUID
from enum import Enum

"""  Base Entity """


class BaseEntity(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: Union[datetime, None] = None


""" Status Schemas """


class StatusBase(BaseModel):
    name: str


class CreateStatus(StatusBase):
    pass


class UpdateStatus(StatusBase):
    pass


class Status(BaseEntity, StatusBase):
    pass

    class Config:
        form_attributes = True


""" User Schema """


class UserBase(BaseModel):
    full_name: str
    phone: Union[str, None] = None


class CreateUser(UserBase):
    email: EmailStr
    password: str


class UpdateUser(UserBase):
    status_id: UUID


class User(BaseEntity, UserBase):
    email: EmailStr
    status_id: UUID

    class Config:
        form_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


""" ToDo Category Schemas """


class TodoCategoryBase(BaseModel):
    name: str


class CreateTodoCategory(TodoCategoryBase):
    pass


class UpdateTodoCategory(TodoCategoryBase):
    pass


class TodoCategory(BaseEntity, TodoCategoryBase):
    pass

    class Config:
        form_attributes = True


""" ToDo Schemas """


class TodoBase(BaseModel):
    title: str
    description: str


class CreateTodo(TodoBase):
    category_id: UUID


class UpdateTodo(TodoBase):
    status_id:  Union[UUID, None] = None


class Todo(BaseEntity, TodoBase):
    status_id:  Union[UUID, None] = None
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
