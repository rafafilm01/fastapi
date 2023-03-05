from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import database, schemas, models, utils, oauth2
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm # used for retrieving user's creds , alternative to using schemas
#NOTE the API now needs to use form data to send and receive info , not the raw /JSON format 

router = APIRouter(tags=['authentication'])

@router.post('/login', response_model=schemas.Token)
#### CODE REVISION  ###  replacing the usage of schemas with OAuth2PasswordRequestForm  
# def login( user_credentials: schemas.UserLogin,  db: Session = Depends(database.get_db)):
def login (user_credentials :OAuth2PasswordRequestForm = Depends() , db : Session= Depends(database.get_db)):
    #attempt to match the user with the db
    #### CODE REVISION  ###  replacing the usage of schemas with OAuth2PasswordRequestForm email field is not used by OAuth2PasswordRequestForm and would not have a match. Instead we need to use username
    #user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    print("*** user signed in, happy tests ! *** ")
    
    if not user: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Invalid credentials !")
    
    #compare the password provided by the user with the hashed version to see if there is a match 
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials !")
    
    #create a token
    access_token = oauth2.create_access_token(data= {'user_id' : user.id})
    #return the token 
    return {"access_token" : access_token , "token_type" : "bearer"}
