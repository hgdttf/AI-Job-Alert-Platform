from pydantic import BaseModel
from pydantic import EmailStr

from typing import List


class UserCreate(BaseModel):

    email: EmailStr
    categories: List[str]
    delivery_time: str