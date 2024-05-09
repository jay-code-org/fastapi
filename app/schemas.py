from datetime import datetime
from enum import Enum
from typing import Union
from pydantic import BaseModel, EmailStr
from uuid import UUID

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


""" Role Schemas """


class RoleBase(BaseModel):
    name: str


class CreateRole(RoleBase):
    pass


class UpdateRole(StatusBase):
    pass


class Role(BaseEntity, RoleBase):
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
    role_id: UUID

    class Config:
        form_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


""" Category Schemas """


class CategoryBase(BaseModel):
    name: str


class CreateCategory(CategoryBase):
    pass


class UpdateCategory(CategoryBase):
    pass


class Category(BaseEntity, CategoryBase):
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
    status_id:  UUID
    category_id:  UUID
    owner_id: UUID
    owner: User

    class Config:
        form_attributes = True


""" Access Token Schemas """


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: str
    id: str


""" Status Enum"""


class StatusEnum(Enum):
    New = "New"
    Blocked = "Blocked"
    Deleted = "Deleted"
    Completed = "Completed"
    Active = "Active"
    Suspended = "Suspended"
    Terminated = "Terminated"


""" Category Enum"""


class CategoryEnum(Enum):
    Coding = "Coding"
    Sports = "Sports"
    Cooking = "Cooking"


""" Role Enum"""


class RoleEnum(Enum):
    Admin = "Admin"
    User = "User"
