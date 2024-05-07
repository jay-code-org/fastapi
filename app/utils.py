

import bcrypt
from fastapi import Depends
from sqlalchemy import UUID
from sqlalchemy.orm import Session

from .database import get_db
from . import models


def find_todo(id: UUID, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == id)
    return todo


# Hash a password using bcrypt
def hash_password(password):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password


# Check if the provided password matches the stored password (hashed)
def verify_password(plain_password, user_password):

    password_byte_enc = plain_password.encode('utf-8')
    return bcrypt.checkpw(password=password_byte_enc, hashed_password=user_password)
