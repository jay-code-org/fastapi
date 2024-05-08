from fastapi import APIRouter,status,Depends,HTTPException
import psycopg2
from .. import schemas,models,database 
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/statuses",tags=["Status"])

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Status)
def create_status(create_status:schemas.CreateStatus,db:Session = Depends(database.get_db)):
    status_dict = create_status.model_dump()
    new_created_status = models.Status(**status_dict)

    try:
        db.add(new_created_status)
        db.commit()
        db.refresh(new_created_status)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Status name '{create_status.name}' already exist")    

    return new_created_status

