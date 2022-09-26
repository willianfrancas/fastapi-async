from typing import Optional, List
from pydantic import BaseModel, EmailStr

from schemas.article_schema import ArticleSchema


class UserSchemaBase(BaseModel):
    id: Optional[int] = None
    name: str
    lastname: str
    email: EmailStr
    is_admin: bool = False

    class Config:
        orm_mode = True


class UserSchemaCreate(UserSchemaBase):
    pwd: str


class UserSchemaArticles(UserSchemaBase):
    articles: Optional[List[ArticleSchema]]


class UserSchemaUpdate(UserSchemaBase):
    name: Optional[str]
    lastname: Optional[str]
    email: Optional[EmailStr]
    pwd: Optional[str]
    is_admin: Optional[bool]
