from typing import Optional
from uuid import UUID
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2, database

router = APIRouter(prefix="/todos", tags=["Todos"])

# Get Todo List


@router.get("/", response_model=list[schemas.Todo], status_code=status.HTTP_200_OK)
def get_todos(
    db: Session = Depends(database.get_db),
    user: schemas.TokenData = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    todos = (
        db.query(models.Todo)
        .filter(models.Todo.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return todos

# Create Todo


@router.post("/", response_model=schemas.Todo, status_code=status.HTTP_201_CREATED)
def create_todo(
    create_todo: schemas.CreateTodo,
    db: Session = Depends(database.get_db),
    user: schemas.TokenData = Depends(oauth2.get_current_user),
):

    todo_status = db.query(models.Status).filter(
        models.Status.name == schemas.StatusEnum.New.value).first()

    if todo_status is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Something went wrong")

    todo_category = db.query(models.Category).filter(
        models.Category.id == create_todo.category_id).first()

    if todo_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with ID: {create_todo.category_id} not found")

    todo = models.Todo(owner_id=user.id,
                       status_id=todo_status.id, **create_todo.model_dump())

    try:
        db.add(todo)
        db.commit()
        db.refresh(todo)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unable to perform specified operation")

    return todo


# Get Todo By ID
@router.get("/{id}", response_model=schemas.Todo, status_code=status.HTTP_200_OK)
def get_todo(
    id: UUID,
    db: Session = Depends(database.get_db),
    user: schemas.TokenData = Depends(oauth2.get_current_user),
):
    todo = db.query(models.Todo).filter(models.Todo.id == id).first()

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id '{id}' not found",
        )

    return todo

# Update Todo


@router.put("/{id}", response_model=schemas.Todo, status_code=status.HTTP_200_OK)
def update_todo(
    id: UUID,
    update_todo: schemas.UpdateTodo,
    db: Session = Depends(database.get_db),
    user: schemas.TokenData = Depends(oauth2.get_current_user),
):
    todo_query = db.query(models.Todo).filter(models.Todo.id == id)
    if todo_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id '{id}' not found",
        )

    if UUID(user.id) != todo_query.first().owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    new_data = update_todo.model_dump()
    new_data.update(
        {
            "updated_at": datetime.now(timezone.utc)
        }
    )

    todo_query.update(new_data, synchronize_session=False)

    db.commit()

    return todo_query.first()

# Delete Todo


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    id: UUID,
    db: Session = Depends(database.get_db),
    user: schemas.TokenData = Depends(oauth2.get_current_user),
):

    todo_query = db.query(models.Todo).filter(models.Todo.id == id)

    if todo_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id '{id}' not found",
        )

    if UUID(user.id) != todo_query.first().owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    todo_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
