from typing import List
from pydantic import BaseModel

from models.MethodModel import MethodModel

class SendMessageMethodModel(MethodModel):
    method: str = "send_message"
    conversation_id: str
    encrypted_message_content: str