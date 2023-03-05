from jose import JWTError, jwt  
from datetime import datetime, timedelta
from .import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings

#used to get_current_user function
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#secret_key
#algorithm
#expiration_time

# NOTE normally stored these as env variables 
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

#function that creates the encoded JWT. JWT consists of data payload and token expiry date, secret key and the type of algorithm  that is used  
def create_access_token (data : dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() +timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

#function that verifies the access token
def verify_access_token( token : str , credentials_exception): # pass in the token that will be verified and the exception in case there is no token or it does not pass the verification 
    try:
        #store the payload data
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        #extract the specific field based on what is being generated for the access token in auth.py
        id : str = payload.get('user_id')
        
        if id is None: 
            raise credentials_exception

        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data
    
def get_current_user(token : str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)
