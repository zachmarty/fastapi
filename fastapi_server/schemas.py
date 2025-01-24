from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    article: int
    price: float
    rating: float
    amount: int


class ArticleBase(BaseModel):
    article: int
