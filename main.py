from typing import Any, Dict, List
from config import DEBUG
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from models.CreatePrivateConversationMethodModel import CreatePrivateConversationMethodModel
from models.MethodModel import MethodModel
from models.SendMessageMethodModel import SendMessageMethodModel
import rltproto
import view
import json
from pydantic.tools import parse_obj_as

app = FastAPI(debug=DEBUG, routes=view.routes)
app.mount("/static", StaticFiles(directory="view/static"), name="static")

connection_manager = rltproto.ConnectionManager()
rltproto_manager = rltproto.RLTProto(connection_manager)

@app.websocket("/rltproto/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await rltproto_manager.listen_proto(websocket, user_id)