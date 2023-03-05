from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2



router = APIRouter(prefix='/vote', tags=['Vote'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote( vote : schemas.Vote, db : Session = Depends(database.get_db), current_user : int = Depends(oauth2.get_current_user)):
    
    #check if the post exists in the first place
    post = db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    print(type(post))
    if not post : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"the post  {vote.post_id} does not exist and cannot be voted on ")
    
    #a check to see if existing user (that is currently signed in ) has not voted on this post already , 2 conditions are being passed for validation in .filter()
    vote_query = db.query(models.Vote).filter(models.Vote.post_id==vote.post_id, models.Vote.user_id==current_user.id)
    found_vote = vote_query.first()
    #direction provided by the user is 1 - he wants to leave a like on the post
    if( vote.dir ==1) :
        if found_vote : 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="It is not possible to vote on the same item 2x ")
        
        #if this is the 1st vote on this post by logged in user , register it under new_vote and add it to the Vote table
        new_vote = models.Vote(post_id= vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message" : "vote added "}
    
       
    else:
        #the vote does not exist 
        if not found_vote: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist ! ")
        
        #the vote exists and the user wants to remove it (delete his like)
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message' : "successfully deleted the vote"}
    