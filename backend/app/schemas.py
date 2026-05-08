from pydantic import BaseModel
from typing import List


class UserCreate(BaseModel):

    email: str
    categories: List[str]
    delivery_time: str