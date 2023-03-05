from .. import models , schemas, utils, oauth2
from .. database import get_db
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.sql.functions import func #used for more complex SLA queries 
from sqlalchemy.orm import Session
from typing import Optional, List


router = APIRouter(prefix='/posts', tags =['posts'])

# @router.get('/', response_model= List[schemas.Post])
@router.get('/', response_model= schemas.PostOut)
def get_posts(db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user),  limit : int =10, skip : int  = 0, search : Optional[str] = ""):
    
    #passing a query parameter from the header into the function , the URL in this  case is http://posts?limit=3 any additional params can be added later in the url with & e.g http://posts?limit=3&skip=2
    # print(limit) #the value accessed by the user can be seen in the code and used further, in this case to limit the number of posts on the website
    
    #OLD CODE , would bring up all of the posts from the table, db.query(models.Post) gets us access to Posts, from there we can either get all of them .all() or focus on filtering further .filter()
   # posts = db.query(models.Post).all()
    
    #NEW CODE - shows the posts but applies limit the user has specified (of the default one) 
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # a more advanced SLQ query with table JOIN , joining Posts and Votes with a common denominator being post_id (from Vote) and id (from Post)
    # result = db.query(models.Post, func.count(models.Vote.post_id).label("total votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    # print(result)
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    # print(result)
    
    
    return results
    # return result
 
#it is possible to use the same URL for get and post requests . By default get gets priority , the prio changes when there is data added to the URl which in this case would indicate a put request 
#additional status_code provided so that 201 confirmation gets sent to the client instead of 200
@router.post('/', status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post : schemas.PostCreate, db : Session = Depends(get_db), current_user : str = Depends(oauth2.get_current_user)):
    print(post)     #print line to see the results in py 
    print("************")   #print line to see the results in py
    print(post.dict())  #print line to see the results in py
    
    #creating a new post and saving it in the table NOTE db.add , db.commit and db.refresh needed at the end to deliver / save and return the new post   
    
    print (current_user.id)
   #NOTE 1: 2 ways to create a new post 1. by creating and unpacking a dictionary based on Post model for easier field assignment  
   # NOTE including owner_id as current_user.id in order to auto populate the field as the user who is creating a post 
    new_post = models.Post(owner_id =current_user.id, **post.dict())
    #NOTE 2 : manually assigning the values, works ok as well but can be troublesome with bigger models that have a lot of columns
    # new_post = models.Post(title= post.title, content =post.content, published = post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
#set what type of data is allowed in the POST request
#title str, content str
    
    

    
#function for retrieving 1 individual post (using ID)
# @router.get("/{id}", response_model= schemas.Post) #STANDARD SQL 

@router.get("/{id}", response_model= schemas.PostOut) # SQL JOIN 
def get_post(id : int , db : Session = Depends(get_db) , user_id : str = Depends(oauth2.get_current_user)):
    print(id)   #print the ID to verify correct value was passed from the URL / decorator
    
    # NOTE : OLD CODE using the logic from find post function we can pull out details of the specific post 
    # post = find_post(id)
    
    
    #STANDARD SQL
    post = db.query(models.Post).filter(models.Post.id ==id).first() #STANDARD SQL
    
    
    # SQL JOIN NOTE still problems with SQL JOIN logic
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id ==id).first() 
    #custom made response if there is no match for the ID , this changes the status code sent from the fastAPI to the client, utlizes HTTPException with if not logic
    if not post: #if the post id does not exist in my_posts
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id:{id} was not found")
    
    # post_votes = post["votes"]
    # print(post_votes)
    return post



######route to delete a post  ######
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post (id : int,  db : Session = Depends(get_db), current_user : str = Depends(oauth2.get_current_user)):
    #deleting the post logic
    #1st - find the index in the array that has the required array using the find_index_post function
    # index = find_index_post(id)

    post_query = db.query(models.Post).filter(models.Post.id ==id)
    post = post_query.first()
    #logic to catch cases where index is not found (does not exist) when trying to delete a post 
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with the ID {id} does not exist')
    #logic to check if the user is trying to delete their own posts or other persons (which is restricted)
    if int(post.owner_id) != int(current_user.id) :
        print(type(post.owner_id))
        print(type(current_user.id))
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not authorized to remove other users posts")
        
    
    #removing the post 
    post_query.delete(synchronize_session=False)
    db.commit()
    
    #removing of the post using pop
    # my_posts.pop(index)
    # BEST PRACTICE - when deleting something we do not send data back (like messages). Instead we send back a confirmation code 
    ## return {"message ": "post was successfully deleted "}
    return Response(status_code= status.HTTP_204_NO_CONTENT)


#### route to update the post  - 2 types of put request - put / patch
@router.put("/{id}", response_model= schemas.Post)
def update_post(id :int, updated_post :schemas.PostCreate,  db : Session = Depends(get_db) , current_user : str = Depends(oauth2.get_current_user)):
    # index = find_index_post(id)
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
   #logic to catch cases where index is not found (does not exist) when trying to update a post 
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with the ID {id} does not exist')
    
    #logic to check if the user is trying to update their own posts or other persons (which is restricted)
    if int(post.owner_id) != int(current_user.id) :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not authorized to edit other users posts")
    #logic to update the existing post (once the ID matches)
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    #convert to a regular python dictionary 
    # post_dict = post.dict()
    # post_dict["id"] = id
    # my_posts[index] = post_dict
    return post_query.first()
