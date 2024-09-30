# app/shanyraks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import schemas, crud, models
from .auth import get_current_user
from .database import get_db

router = APIRouter()

# Маршруты для объявлений (Shanyraks)

@router.post("/shanyraks/", response_model=schemas.ShanyrakResponse)
def create_shanyrak(shanyrak: schemas.ShanyrakCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_shanyrak(db=db, shanyrak=shanyrak, user_id=current_user.id)

@router.get("/shanyraks/{shanyrak_id}", response_model=schemas.ShanyrakDetail)
def read_shanyrak(shanyrak_id: int, db: Session = Depends(get_db)):
    shanyrak = crud.get_shanyrak(db, shanyrak_id)
    if not shanyrak:
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    total_comments = db.query(models.Comment).filter(models.Comment.shanyrak_id == shanyrak_id).count()
    shanyrak_response = schemas.ShanyrakResponse(
        id=shanyrak.id,
        type=shanyrak.type,
        price=shanyrak.price,
        address=shanyrak.address,
        area=shanyrak.area,
        rooms_count=shanyrak.rooms_count,
        description=shanyrak.description,
        user_id=shanyrak.user_id,
        total_comments=total_comments
    )
    return shanyrak_response

@router.get("/shanyraks/", response_model=List[schemas.ShanyrakResponse])
def read_shanyraks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    shanyraks = crud.get_shanyraks(db, skip=skip, limit=limit)
    response = []
    for sh in shanyraks:
        total_comments = db.query(models.Comment).filter(models.Comment.shanyrak_id == sh.id).count()
        response.append(
            schemas.ShanyrakResponse(
                id=sh.id,
                type=sh.type,
                price=sh.price,
                address=sh.address,
                area=sh.area,
                rooms_count=sh.rooms_count,
                description=sh.description,
                user_id=sh.user_id,
                total_comments=total_comments
            )
        )
    return response

@router.patch("/shanyraks/{shanyrak_id}", status_code=200)
def update_shanyrak(shanyrak_id: int, shanyrak: schemas.ShanyrakUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    updated_shanyrak = crud.update_shanyrak(db, shanyrak_id, shanyrak, current_user.id)
    if not updated_shanyrak:
        raise HTTPException(status_code=404, detail="Объявление не найдено или у вас нет прав на его изменение")
    return {"detail": "Объявление обновлено успешно"}

@router.delete("/shanyraks/{shanyrak_id}", status_code=200)
def delete_shanyrak(shanyrak_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    success = crud.delete_shanyrak(db, shanyrak_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Объявление не найдено или у вас нет прав на его удаление")
    return {"detail": "Объявление удалено успешно"}

# Маршруты для комментариев

@router.post("/shanyraks/{shanyrak_id}/comments", status_code=200)
def create_comment(shanyrak_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    shanyrak = crud.get_shanyrak(db, shanyrak_id)
    if not shanyrak:
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    crud.create_comment(db, comment, shanyrak_id, current_user.id)
    return {"detail": "Комментарий добавлен успешно"}

@router.get("/shanyraks/{shanyrak_id}/comments", response_model=List[schemas.CommentResponse])
def get_comments(shanyrak_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    comments = crud.get_comments(db, shanyrak_id, skip=skip, limit=limit)
    return comments

@router.patch("/shanyraks/{shanyrak_id}/comments/{comment_id}", status_code=200)
def update_comment(shanyrak_id: int, comment_id: int, comment: schemas.CommentUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    updated_comment = crud.update_comment(db, comment_id, comment, current_user.id)
    if not updated_comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден или у вас нет прав на его изменение")
    return {"detail": "Комментарий обновлен успешно"}

@router.delete("/shanyraks/{shanyrak_id}/comments/{comment_id}", status_code=200)
def delete_comment(shanyrak_id: int, comment_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    success = crud.delete_comment(db, comment_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Комментарий не найден или у вас нет прав на его удаление")
    return {"detail": "Комментарий удален успешно"}
