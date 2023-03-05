#additional tools 
#password hashing
from passlib.context import CryptContext



################## password hashing  set up ############### setting up the default encryption method
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
################## password hashing  set up ###############

#custom function used in main.py for password hashing 
def hash(password):
    return pwd_context.hash(password)

#function that will be used at the login stage , will take the password the user provides, hash it and compare it to the password of a user in DB once a match is made 
def verify (plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)