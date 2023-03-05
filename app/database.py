#used for setting up the connection between sqlalchemy and potgresql, use a custom made URI for the postgreDB, engine to connect to the DB (using the URI) and sessionLocal to make one of sessions when routing / pathing to the give API calls in main.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

#connection string for SQL alchemy
# EXAMPLE OF A STRING --> SQLALCHEMY_DATABASE_URL = 'postresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}./{settings.database_name}"
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost/fastapi'
#engine that connects to the  sql alchemy to postgres DB
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# in order to talk to the DB we use session 
SessionLocal = sessionmaker(autocommit =False, autoflush=False, bind=engine)

Base = declarative_base()

############### dependency for SQL alchemy session #################
#to be used as part of other functions that require active session in order to make changes to the db tables
def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

############### dependency for SQL alchemy session #################


#### CODE NO LONGER IN USE , LEFT AS A REMINDER / RE-USE
#### CODE NO LONGER IN USE , LEFT AS A REMINDER / RE-USE
#### CODE NO LONGER IN USE , LEFT AS A REMINDER / RE-USE
#### CODE NO LONGER IN USE , LEFT AS A REMINDER / RE-USE
import time 
import psycopg2
from psycopg2.extras  import RealDictCursor
#while loop to keep trying to connect to the DB if the connection was unsuccessful.  LOGIC -> there is no point in starting the app if the connection to the data has not been made correctly . If the try condition is met , we will break out of a loop with BREAK , otherwise except logic will kick in , give us an error code and attempt the while loop in 5 seconds due to time.sleep(5)
#setting up connection to local PG DB 
while True:
    try : 
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='admin', cursor_factory=RealDictCursor)
        cursor = conn.cursor() #cursor will be used to execute sql statements 
        print ("database connection was successful")
        break

    except Exception as error:
        print("Unable to connect to the database")
        print(f"Error : {error}")
        print("retrying connection in 5 seconds ...")
        time.sleep(5)    
    #array to store posts (before we starting using a DB), at the momeent hardcoded to test get functionality 
    my_posts =[{"title" : "title of post 1", "content": "this is the content of the 1st post ", "id":1 },
            {"title" : "title of post 2", "content": "this is the content of the 2nd post ", "id":2 }]

