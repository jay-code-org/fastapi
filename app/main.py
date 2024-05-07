from fastapi import FastAPI
from .database import engine
from . import models
from .routers import user, todo, auth

# This line makes sure all models are applied in the database before running the app
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(todo.router)


@app.get("/test")
def root():
    return {"message": "Success"}
