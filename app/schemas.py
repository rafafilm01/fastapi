from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint # used to restrict the values to 0 and 1 in the voting schema

#class used for pydantic / basemodel validation , to be used in @app.post,  ensures right type of data is benign sent in the post requests;
# used for local files , later to be replaced by models.py - sqlalchemy


########### schema for users #################
class UserCreate (BaseModel):
    email : EmailStr
    password : str
    
###### response schema for users (to remove the password from the reply) ######

class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    class Config:
        orm_mode = True
        
################# schemas for users sending data ###############
class PostBase(BaseModel):
    title : str
    content : str
    #optional field for the schema with default value set to True 
    published : bool =True
    #optional value for the scheme with None as the default value
    # rating : Optional[int] = None
    
class PostCreate(PostBase):
    pass

############### schemas for responses ############################## 
#creating a dedicated schemas for responses allows us to limit the amount and type of data being passed back or sent . E. G. in cases of users creating a new account we should not have to / need to pass back the password that has been created. 
class Post(PostBase):
   
    id : int
    created_at : datetime
    owner_id : int
    owner : UserOut
    
    class Config:
        orm_mode = True
        #orm_mode will tell the pydantic model to read the data even if it is not a dict bur an ORM model (SQLALchemy) , otherwise it will generate an  value is not a valid dict (type=type_error.dict) ERROR
        

#### schema for post + votes results using SQL joins
#NOTE PROBLEM WITH PostOut SCHEMA LOGIC NOT GETTING ANY RESULTS - issue with nesting answers under posts 
class PostOut (PostBase):
    Post : Optional[Post]
    votes : Optional[int] 
    title : Optional[str]
    content : Optional[str]
        
    class Config:
        orm_mode = True
        
        
############ post schema for login ##########
class UserLogin (BaseModel):
    email : EmailStr
    password : str
    
    
##### schema for access token #####
class Token(BaseModel):
    access_token : str
    token_type : str
   
    
##### schema for token data (that will be embedded in the access token) #####
class TokenData(BaseModel) :
    id : Optional[str] = None


#### schema for voting data ####
class Vote(BaseModel): 
    
    post_id : int
    dir : conint(le=1)
    #user_id will be provided by the user being authenticated ( you vote for something as yourself) 