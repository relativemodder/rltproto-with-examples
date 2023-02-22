from typing import List
from pydantic import BaseModel

class EncryptedMessageEventModel(BaseModel):
    event_type: str = "encrypted_message"
    enrypted_content: str
    from_user_id: str