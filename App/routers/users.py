from fastapi import FastAPI, Response, status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..dataBase import get_db
from ..import models,schemas,utils

router=APIRouter(
    prefix="/users",
    tags=['users']
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.userOut)
def create_user(user:schemas.userCreate, db:Session= Depends(get_db)):
    hashed_password= utils.hash(user.password)
    user.password =hashed_password
    new_user =models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.userOut)
def get_Users(id: int,db:Session= Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id: {id} does not exist")
    
    return user