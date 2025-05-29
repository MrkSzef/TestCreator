from __future__ import annotations
from abc import ABC, abstractmethod
from asyncio import Queue, QueueFull
from typing import Any

from datamodel import CallbackMessageType, TestInfoResponse
    
class CallbackMessage:
    def __init__(self, typ: CallbackMessageType, data: Any) -> None:
        self.typ: CallbackMessageType = typ
        self.data: Any = data
    
    def __str__(self) -> str:
        return f"CallbackMessage(data={self.data})"
    
    def __repr__(self) -> str:
        return f"CallbackMessage(data={self.data})"
                
class CallbackEntity(ABC):
    def __init__(self, que: Queue) -> None:
        self._que: Queue = que 
    
    def __str__(self) -> str:
        return f"BasicCallback(que={self._que})"
    
    def __repr__(self) -> str:
        return f"BasicCallback(que={self._que})"
        
    def __full_que_msg__(self) -> str:
        return f"Que jest pełne. Nie można dodać danych. Que: {self._que}"
    
    @abstractmethod
    def __call__(self, typ: CallbackMessageType, test_info: TestInfoResponse) -> None:
        ...
        
class InfoCallback(CallbackEntity):
    def __call__(self, typ: CallbackMessageType, test_info: TestInfoResponse) -> None:
        try:
            self._que.put_nowait(CallbackMessage(typ=typ, data=test_info.model_dump()))
        except QueueFull:
            print(self.__full_que_msg__())

class WynikCallback(CallbackEntity):
    def __call__(self, typ: CallbackMessageType, test_info: TestInfoResponse) -> None:
        try:
            self._que.put_nowait(CallbackMessage(typ=typ, data=[model.model_dump() for model in test_info.uczestnicy_odpowiedzi]))
        except QueueFull:
            print(self.__full_que_msg__())