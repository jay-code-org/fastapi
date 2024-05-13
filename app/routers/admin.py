from fastapi import status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database, utils

router = APIRouter(prefix="/admin", tags=["Admin"], include_in_schema=False)


@router.post('/', response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(create_user: schemas.CreateUser, db: Session = Depends(database.get_db), ):

    check_user = db.query(models.User).filter(
        models.User.email == create_user.email).first()

    if check_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Email {create_user.email} already exist")

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

    new_user = create_user.model_dump()
    new_user.update({"password": utils.hash_password(
        create_user.password), "status_id": user_status.id, "role_id": user_role.id})

    user = models.User(**new_user)

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unable to perform specified operation")

    return user
