from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm.session import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Hashing user.password
    user.password = utils.hash(user.password)

    new = models.User(**user.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
    return user
