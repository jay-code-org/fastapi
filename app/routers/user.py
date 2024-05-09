from fastapi import APIRouter, status, Depends, HTTPException
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, DatabaseError, OperationalError, NotSupportedError, ProgrammingError
from datetime import datetime
from .. import schemas, models, utils, oauth2
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post('/', response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(create_user: schemas.CreateUser, db: Session = Depends(get_db), ):

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
        models.Role.name == schemas.RoleEnum.User.value).first()

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


@router.put('/{id}', response_model=schemas.User, status_code=status.HTTP_200_OK)
def update_user(id: UUID, update_user: schemas.UpdateUser, db: Session = Depends(get_db), user: schemas.TokenData = Depends(oauth2.get_current_user)):

    user = db.query(models.User).filter(models.User.id == id)

    if user.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} not found")

    new_data = update_user.model_dump()
    new_data.update({"updated_at": datetime.now()})

    user.update(new_data, synchronize_session=False)

    db.commit()

    return user.first()
