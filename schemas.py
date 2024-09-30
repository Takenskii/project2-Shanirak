from pydantic import BaseModel
from typing import Optional, List

class ShanyrakCreate(BaseModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str

class ShanyrakResponse(BaseModel):
    id: int
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    user_id: int

    class Config:
        orm_mode = True


class CommentCreate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    content: str
    created_at: str
    author_id: int

    class Config:
        orm_mode = True

class ShanyrakWithComments(ShanyrakResponse):
    comments: List[CommentResponse]
    total_comments: int
