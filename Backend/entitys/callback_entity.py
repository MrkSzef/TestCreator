from __future__ import annotations
from abc import ABC, abstractmethod
from asyncio import Queue, QueueFull

from datamodel import TestInfoResponse              
                
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
    def __call__(self, data: TestInfoResponse) -> None:
        ...
        
class InfoCallback(CallbackEntity):
    def __call__(self, data: TestInfoResponse) -> None:
        try:
            self._que.put_nowait(data)
        except QueueFull:
            print(self.__full_que_msg__())

class WynikCallback(CallbackEntity):
    def __call__(self, data: TestInfoResponse) -> None:
        try:
            self._que.put_nowait(data.uczestnicy_odpowiedzi)
        except QueueFull:
            print(self.__full_que_msg__())
    