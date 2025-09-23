from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    user_instance = models.User(**user.model_dump())
    db.add(user_instance)
    db.commit()
    db.refresh(user_instance)
    return user_instance


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user_qeury = db.query(models.User).filter(models.User.id == id)
    if not user_qeury.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"item with id: {id} not found",
        )
    return user_qeury.first()
