from fastapi import FastAPI
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
#pydantic and basemodel used to enforce type of responses we will get from our users in the post requests 

#typing / optional used for setting up attributes that are only optional and can be skipped if needed 

from . import models #used when making request calls to the DB





#PostgreSQL adapter for the Python programming language. It is a wrapper for the libpq, the official PostgreSQL client library.
###### libs needed for sqlalchemy ######
from . import models
from .database import engine

from .routers import post, user, auth, vote




############## SQL alchemy and link to the databse.py #############
# models.Base.metadata.create_all(bind=engine)
#NOTE REDUNDANT CODE AS ALEMBIC IS USED TO CREATE DB BASED ON THE MODELS.PY , the db can be created with the 1st alembic revision --autogenerate 
############## SQL alchemy and link to the databse.py #############



app = FastAPI()

#list of all allowed URLs that can talk to our API origins = ["*"] - will allow communication from every single domain/ origin 
origins = ["*"]

##### CORS REQUIREMENT ####
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 ##### CORS REQUIREMENT ####





#importing routers for user and post APIs

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#1st page to verify the api is running 
@app.get('/')
async def root():
    return {'message': 'Hello world woooo !!!'}

