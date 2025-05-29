from __future__ import annotations

from datamodel import CallbackMessageType, TestInfoResponse
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
        else:
            print(f"Callback {callback} nie jest subskrybowany.")
            
    def wyczysc(self) -> None:
        self._callbacks.clear()
            
    def powiadom(self, typ: CallbackMessageType , test_info: TestInfoResponse) -> None:
        for callback in self._callbacks:
            if isinstance(callback, CallbackEntity):
                try:
                    callback(typ, test_info)
                except Exception as e:
                    print(f"Błąd podczas wywoływania callbacka {callback}: {e}")
            else:
                print(f"Nieprawidłowy callback: {callback}")
            
        
        