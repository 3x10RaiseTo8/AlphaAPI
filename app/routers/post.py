from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from sqlalchemy.sql.functions import func
from sqlalchemy.orm import aliased
from .. import models, schemas, oauth2
from typing import List, Optional
from ..database import get_db
from sqlalchemy.orm.session import Session

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostVote])
def get_posts(db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    # post_alias = aliased(models.Post, name="post_details")
    # print("post_alias:", post_alias)
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new = cursor.fetchone()
    # conn.commit()

    new = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@router.get("/{id}", response_model=schemas.PostVote)
def get_post(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):

    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with id {id} doesn't exist")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):

    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} id not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform this request")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_posts(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, id))
    # updated = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    check_post = post_query.first()

    if check_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} id not found")

    if check_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform this request")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
