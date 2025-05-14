from __future__ import annotations
from pydantic import BaseModel
from typing import Optional

type U_ID_t = str
type T_ID_t = str
type P_ID_t = int

class Uczen(BaseModel):
    U_ID: U_ID_t
    IMIE: str
    NAZWISKO: str
    DZIENIK_ODPOWIEDZI: dict[P_ID_t, str] # Id pytania do udzielonej odpowiedzi

class Pytanie(BaseModel):
    P_ID: P_ID_t
    TEKST: str
    ODPOWIDZI: list[str]

class Test(BaseModel):
    T_ID: T_ID_t
    LISTA_PYTAN: list[Pytanie]
    DZIENIK_UCZNIOW: dict[U_ID_t, Uczen]
    POPRAWNE_ODPOWIEDZI: Optional[dict[P_ID_t, str]] = None
    
