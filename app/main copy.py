from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import uuid

app = FastAPI()


def generate_id():
    return str(uuid.uuid4())


class TodoBase(BaseModel):
    title: str
    description: str


class Todo(TodoBase):
    id: str
    created_at: datetime
    is_completed: bool = False


class CreateTodo(TodoBase):
    pass


class UpdateTodo(TodoBase):
    is_completed: bool


todo_list: list[Todo] = []


def find_todo(id: str):
    for todo in todo_list:
        if todo.id == id:
            return todo


def find_todo_index(id):
    for i, todo in enumerate(todo_list):
        if todo.id == id:
            return i


@app.get('/test')
def root():
    return {"message": "Success"}


@app.get('/todos', status_code=status.HTTP_200_OK)
def get_todos():
    return todo_list


@app.post('/todos', status_code=status.HTTP_201_CREATED)
def create_todo(create_todo: CreateTodo):
    new_todo = Todo(id=generate_id(), created_at=datetime.now(),
                    **create_todo.model_dump())
    todo_list.append(new_todo)

    return new_todo


@app.get("/todos/{id}", status_code=status.HTTP_200_OK)
def get_todo(id: str):
    todo = find_todo(id)

    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Todo with id \'{id}\' not found")

    return todo


@app.put('/todos/{id}', status_code=status.HTTP_200_OK)
def update_todo(id: str, update_todo: UpdateTodo):
    todo = find_todo(id)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Todo with id \'{id}\' not found")

    todo_index = find_todo_index(id)
    todo = todo.model_copy(update=update_todo.model_dump())

    todo_list[todo_index] = todo

    return todo


@app.delete("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: str):

    todo = find_todo(id)
    todo_index = find_todo_index(id)

    if todo is None or todo_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Todo with id \'{id}\' not found")

    todo_list.pop(todo_index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
