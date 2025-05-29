from __future__ import annotations
from fastapi import WebSocket, WebSocketDisconnect
from typing import Self
from asyncio import Queue

from datamodel import CallbackMessageType
from entitys.callback_entity import CallbackEntity, CallbackMessage

class PowiadomieniaWebsocket:
    MAX_QUE_SIZE: int = 5
    def __init__(self, websocket: WebSocket, que_size: int | None = None) -> None:
        self._websocket: WebSocket  = websocket
        self._que: Queue = Queue(maxsize=que_size if que_size is not None else self.MAX_QUE_SIZE)
        
    async def __aenter__(self) -> Self:
        await self._websocket.accept()
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type is not None:
            print(f"Błąd podczas obsługi websocketu: {exc_value}")
        await self._websocket.close()
        
    def stworz_callback(self, callback_class: type[CallbackEntity]) -> CallbackEntity:
        callback_entity: CallbackEntity = callback_class(que=self._que)
        return callback_entity
    
    async def start(self):
        try:
            while True:
                msg: CallbackMessage = await self._que.get()
                if msg.typ == CallbackMessageType.UPDATE:
                    await self._websocket.send_json(msg.data)
                elif msg.typ == CallbackMessageType.DELETE:
                    return
                else:
                    print(f"Nieznany typ wiadomości: {msg.typ}")
        except WebSocketDisconnect:
            pass