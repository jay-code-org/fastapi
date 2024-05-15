from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database, schemas, utils
from .routers import user, todo, auth


# This line makes sure all models are applied in the database before running the app
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(todo.router, prefix="/api")


@app.get("/sync")
def root(db: Session = Depends(database.get_db)):
    check_user = db.query(models.User).filter(
        models.User.email == 'admin@fast.com').first()

    if check_user is None:

        user_status = db.query(models.Status).filter(
            models.Status.name == schemas.StatusEnum.Active.value).first()

        if user_status is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Something went wrong")

        user_role = db.query(models.Role).filter(
            models.Role.name == schemas.RoleEnum.Admin.value).first()

        if user_role is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Something went wrong")

        new_user = {"email": "admin@fast.com",
                    "full_name": "Administrator", "phone": "01234567"}
        new_user.update({"password": utils.hash_password(
            "1234"), "status_id": user_status.id, "role_id": user_role.id})

        user = models.User(**new_user)

        try:
            db.add(user)
            db.commit()
            db.refresh(user)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Unable to perform specified operation")
    return {"message": "Synchronized successfully!"}
