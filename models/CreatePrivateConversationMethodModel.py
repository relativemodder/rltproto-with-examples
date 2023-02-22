from typing import List
from pydantic import BaseModel

from models.MethodModel import MethodModel

class CreatePrivateConversationMethodModel(MethodModel):
    method: str = "create_conversation"
    members: List[str]