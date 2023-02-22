from typing import List
from pydantic import BaseModel

class MethodModel(BaseModel):
    method: str = "create_conversation"