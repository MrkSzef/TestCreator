from typing import Any
from fastapi import HTTPException, status


class HTTP_Not_Implemented(HTTPException):
    def __init__(self, opis: Any | tuple[Any] | None = None, headers=None):
        status_code: int = status.HTTP_501_NOT_IMPLEMENTED
        detail: str = "Nie zaimplementowano" or opis
        super().__init__(status_code, detail, headers)
        

class HTTP_Not_found(HTTPException):
    def __init__(self, opis: Any | tuple[Any], headers=None):
        status_code: int = status.HTTP_404_NOT_FOUND
        super().__init__(status_code, opis, headers)
        

class HTTP_Value_Exception(HTTPException):
    def __init__(self, opis: Any | tuple[Any], headers = None):
        status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY
        super().__init__(status_code, opis, headers)
