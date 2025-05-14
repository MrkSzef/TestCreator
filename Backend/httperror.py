from fastapi import HTTPException

class HTTP_Not_Implemented(HTTPException):
    def __init__(self, headers = None):
        status_code: int = 501
        detail: str = "Nie zaimplementowano"
        super().__init__(status_code, detail, headers)
        
class HTTP_Not_Test_find(HTTPException):
    def __init__(self, headers = None):
        status_code: int = 404
        detail: str = "Nie odnaleziono testu"
        super().__init__(status_code, detail, headers)