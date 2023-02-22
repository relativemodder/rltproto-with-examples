from typing import List
from pydantic import BaseModel

class CreatePrivateConversationEventModel(BaseModel):
    event_type: str = "create_private_conversation"
    conversation_id: str
    private_key: str
    members: List[str]