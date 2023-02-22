from fastapi import WebSocket, WebSocketDisconnect
from typing import Any, List, Dict
import random
import base64
import json
import hashlib

from pydantic import parse_obj_as

from models.CreatePrivateConversationEventModel import CreatePrivateConversationEventModel
from models.CreatePrivateConversationMethodModel import CreatePrivateConversationMethodModel
from models.EncryptedMessageEventModel import EncryptedMessageEventModel
from models.MethodModel import MethodModel
from models.SendMessageMethodModel import SendMessageMethodModel

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = dict()

    async def connect(self, websocket: WebSocket, 
                      user_id: str):
        
        await websocket.accept()
        if self.active_connections.get(user_id) is None:
            self.active_connections[user_id] = list()

        self.active_connections[user_id].append(websocket)

    async def disconnect(self, websocket: WebSocket, 
                   user_id: str):
        
        self.active_connections[user_id].remove(websocket)

    async def send_personal_message(self, message: str, 
                                    websocket: WebSocket):
        
        await websocket.send_text(message)
    
    async def send_personal_message_to_user_id(self, message: str, 
                                               user_id: str):
        
        for websocket in self.active_connections[user_id]:
            await self.send_personal_message(message, websocket)
    
    async def send_json_message_to_user_id(self, message: dict, 
                                           user_id: str):
        
        message_json = json.dumps(message)
        await self.send_personal_message_to_user_id(message_json, user_id)

class RLTProto:
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager
        self.conversation_manager: Dict[str, List[str]] = dict()
    
    async def connect_client_to_proto(self, websocket: WebSocket, user_id: str):
        await self.connection_manager.connect(websocket, user_id)
    
    async def disconnect_client_from_proto(self, websocket: WebSocket, user_id: str):
        await self.connection_manager.disconnect(websocket, user_id)

    async def generate_private_key(self) -> str:
        return hashlib.md5(base64.b64encode(str(random.randint(1111, 9999999999)).encode())).hexdigest()
    
    async def generate_conversation_id(self) -> str:
        return base64.b64encode(str(random.randint(1111, 9999)).encode()).decode()
    
    async def create_private_conversation(self, user_ids: List[str]):
        conversation_id = await self.generate_conversation_id()
        self.conversation_manager[conversation_id] = list()

        private_key = await self.generate_private_key()

        for user_id in user_ids:
            
            event = CreatePrivateConversationEventModel(private_key=private_key, 
                                                        members=user_ids,
                                                        conversation_id=conversation_id)

            self.conversation_manager[conversation_id].append(user_id)

            await self.connection_manager.send_json_message_to_user_id(event.dict(), user_id)

    async def send_message_to_private_conversation(self, conversation_id: str, 
                                                   encrypted_message_content: str, 
                                                   from_user_id: str):
        
        for user_id in self.conversation_manager[conversation_id]:
            encrypted_message = EncryptedMessageEventModel(enrypted_content=encrypted_message_content,
                                                           from_user_id=from_user_id)

            await self.connection_manager.send_json_message_to_user_id(encrypted_message.dict(), user_id)
    
    async def listen_proto(self, websocket: WebSocket, user_id: str):
        await self.connect_client_to_proto(websocket, user_id)

        try:
            while True:
                data_raw = await websocket.receive_text()
                data: Dict[str, (str | Any)] = json.loads(data_raw)
                method = parse_obj_as(MethodModel, data)

                match method.method:
                    case "create_conversation":
                        create_conversation_method = parse_obj_as(CreatePrivateConversationMethodModel, data)
                        member_list: List[str] = create_conversation_method.members

                        await self.create_private_conversation(member_list)
                    case "send_message":
                        send_message_method = parse_obj_as(SendMessageMethodModel, data)
                        
                        await self.send_message_to_private_conversation(send_message_method.conversation_id, 
                                                                                    send_message_method.encrypted_message_content, 
                                                                                    user_id)
        except WebSocketDisconnect:
            await self.disconnect_client_from_proto(websocket, user_id)