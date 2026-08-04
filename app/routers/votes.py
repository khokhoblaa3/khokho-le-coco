from fastapi import APIRouter, Depends, status, HTTPException, Response
from typing import List
from sqlalchemy import func 
from sqlalchemy.orm import Session
from .. import models, schemas, auth2
from ..database import get_db

router = APIRouter(
    prefix = '/votes',
    tags = ['votes']
)

@router.post("/", status_code=status.HTTP_201_CREATED )
def vote(votee : schemas.Vote, db: Session = Depends(get_db), userrr = Depends(auth2.get_current_user)):
    post_query = db.query(models.Posts).filter(models.Posts.id == votee.post_id).first()
    if post_query == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Post doesnt exist")
    wanted_post = db.query(models.Votes).filter(userrr.id == models.Votes.user_id, votee.post_id == models.Votes.post_id)
    if votee.dir == 1:     
        if wanted_post.first() != None: 
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="The vote already exists")
        added_vote = models.Votes(user_id = userrr.id, post_id = votee.post_id)
        db.add(added_vote)
        db.commit()
        return "Vote has been created"
    else: 
        if wanted_post.first() ==None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        wanted_post.delete(synchronize_session=False)
        db.commit()
        return "Vote has been deleted"


@router.get("/piou", response_model=List[schemas.VotesOut])
def get_votes(db : Session = Depends(get_db)):
    #query = db.query(models.Posts, func.count(models.Posts.id).label("votes")).join(models.Votes, models.Posts.id == models.Votes.post_id, isouter=True).group_by(models.Posts.id)
    query = db.query(models.Votes)
    print(query)
    votes = query.all()
    print(votes)
    return votes

@router.get("/count_votes", response_model = List[schemas.Count_votes])
def count_votes(db: Session = Depends(get_db)):
    query = db.query(models.Posts, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Posts.id , isouter=True).group_by(models.Posts.id)
    my_return = query.all()
    return my_return