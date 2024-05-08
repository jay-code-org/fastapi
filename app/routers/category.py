from fastapi import APIRouter,status,Depends,HTTPException
import psycopg2
from .. import schemas,models,database 
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/categories",tags=["Category"])

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Category)
def create_category(create_category:schemas.CreateCategory,db:Session = Depends(database.get_db)):
    category_dict = create_category.model_dump()
    new_created_category = models.Category(**category_dict)

    try:
        db.add(new_created_category)
        db.commit()
        db.refresh(new_created_category)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Category name '{create_category.name}' already exist")    

    return new_created_category

