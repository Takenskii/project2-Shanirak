from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

# Объявления
def create_shanyrak(db: Session, shanyrak: schemas.ShanyrakCreate, user_id: int):
    db_shanyrak = models.Shanyrak(**shanyrak.dict(), owner_id=user_id)
    db.add(db_shanyrak)
    db.commit()
    db.refresh(db_shanyrak)
    return db_shanyrak

def get_shanyrak(db: Session, shanyrak_id: int):
    return db.query(models.Shanyrak).filter(models.Shanyrak.id == shanyrak_id).first()

def update_shanyrak(db: Session, shanyrak_id: int, shanyrak_data: schemas.ShanyrakCreate):
    db_shanyrak = get_shanyrak(db, shanyrak_id)
    if db_shanyrak:
        for key, value in shanyrak_data.dict().items():
            setattr(db_shanyrak, key, value)
        db.commit()
        db.refresh(db_shanyrak)
    return db_shanyrak

def delete_shanyrak(db: Session, shanyrak_id: int):
    db_shanyrak = get_shanyrak(db, shanyrak_id)
    if db_shanyrak:
        db.delete(db_shanyrak)
        db.commit()

# Комментарии
def create_comment(db: Session, comment: schemas.CommentCreate, shanyrak_id: int, author_id: int):
    db_comment = models.Comment(content=comment.content, created_at=str(datetime.utcnow()), shanyrak_id=shanyrak_id, author_id=author_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments_by_shanyrak(db: Session, shanyrak_id: int):
    return db.query(models.Comment).filter(models.Comment.shanyrak_id == shanyrak_id).all()

def update_comment(db: Session, comment_id: int, new_content: str):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment:
        db_comment.content = new_content
        db.commit()
        db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment:
        db.delete(db_comment)
        db.commit()

