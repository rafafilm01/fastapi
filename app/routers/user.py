from .. import models , schemas, utils
from .. database import get_db
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session


router = APIRouter(prefix='/users', tags=['users'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user : schemas.UserCreate,  db : Session = Depends(get_db)):
    
    ### hash the password - user.password ###
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    ### hash the password - user.password ###
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

#retrieve the info on a specific user using their ID 
@router.get("/{id}", response_model=schemas.UserOut)
def getUser(id : int, db : Session = Depends(get_db) ):
    user = db.query(models.User).filter(models.User.id ==id).first()
    
    if not user: #if the user id does not exist in users table
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"user with id:{id} was not found")
    
    return user
    
    