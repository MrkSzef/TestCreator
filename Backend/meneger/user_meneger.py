from __future__ import annotations
from typing import Any, Optional
from uuid import uuid4

from datamodel import (
    UUID_Test_t,
    UUID_Urzytkownik_t,
    UzytkonikTyp,
    imie,
    nazwisko
)

class User:
    def __init__(self, ID: UUID_Test_t, 
                 typ: UzytkonikTyp,
                 imie: imie, 
                 nazwisko: nazwisko, 
                 dodatkowe_info: Optional[dict[str, Any]] =  None):
        self.ID: UUID_Urzytkownik_t = ID
        self.typ: UzytkonikTyp = typ
        
        self.imie: imie = imie
        self.nazwisko: nazwisko = nazwisko
        
        self.testy: list[UUID_Test_t] = []
        self.dodatkowe_info: Optional[dict[str, Any]] = dodatkowe_info

class UserMenadzer:
    def __init__(self):
        self.slownik_urzutkownikow: dict[UUID_Urzytkownik_t, User] = {}
        
    def _add(self, urztkownik: User) -> None:
        if urztkownik.ID in self.slownik_urzutkownikow:
            raise ValueError("Urztkonik o podanym id już istnieje", f"ID: {urztkownik.ID}")
        
        self.slownik_urzutkownikow[urztkownik.ID] = urztkownik
    
    def stworz_uzytkownika(self, imie: imie, nazwisko: nazwisko, typ: UzytkonikTyp, dodatkowe_info: Optional[dict[str, Any]] = None) -> UUID_Urzytkownik_t:
        ID: UUID_Urzytkownik_t = uuid4().hex
        
        uzytkonik: User = User(ID=ID, typ=typ, imie=imie, nazwisko=nazwisko, dodatkowe_info=dodatkowe_info)
        self._add(urztkownik=uzytkonik)
        
        return uzytkonik.ID
    
    def get(sefl, ID: UUID_Urzytkownik_t) -> User:
        uzytkonik: User = sefl.slownik_urzutkownikow.get(ID)
        if not uzytkonik:
            raise ValueError("Użytkonik o podanym id nie istnieje",
                             f"ID: {ID}")
            
        return uzytkonik 