from __future__ import annotations
from typing import Any

from entitys.callback_entity import CallbackEntity

class CallbackRegister:
    def __init__(self) -> None:
        self._callbacks: list[CallbackEntity] = []
    
    def __str__(self) -> str:
        return f"CallbackRegister(callbacks={self._callbacks})"
    
    def __repr__(self) -> str:
        return f"CallbackRegister(callbacks={self._callbacks})"
        
    def subskrybuj(self, callback: CallbackEntity) -> None:
        if callback not in self._callbacks:
            self._callbacks.append(callback)
            
    def odsubskrybuj(self, callback: CallbackEntity) -> None:
        if callback in self._callbacks:
            self._callbacks.remove(callback)
            
    def powiadom(self, *args: Any, **kwargs: Any) -> None:
        for callback in self._callbacks:
            try:
                callback(*args, **kwargs)
            except Exception as e:
                print(f"Błąd podczas wywoływania callbacka: {e}")