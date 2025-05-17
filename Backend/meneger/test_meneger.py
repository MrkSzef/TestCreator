from __future__ import annotations
from uuid import uuid4
from random import sample

# Lokalne pliki
from meneger.user_meneger import User
from meneger.file_meneger import PlikMenadzer
from datamodel import (ID_Odp_t, ID_Pytanie_t,
                       UUID_Urzytkownik_t, UUID_Test_t, 
                       Odp_Klucz_t, Odp_lista_t, Odp_t,
                       PytanieResponse,
                       ArkuszResponse, UzytkonikTyp)

class Pytanie:
    def __init__(self, ID: ID_Pytanie_t, tresc: str, odp: Odp_lista_t, odp_praw: Odp_t):
        self.ID: ID_Pytanie_t = ID
        
        self.tresc: str = tresc
        self.odp: Odp_lista_t = odp
        self.odp_praw: Odp_t = odp_praw
    
class Test:
    def __init__(self, ID: UUID_Test_t,
                 pytania_na_arkusz: int,
                 pytania: dict[ID_Pytanie_t, Pytanie],
                 klucz_odp: Odp_Klucz_t,
                 uczestnicy: dict[UUID_Urzytkownik_t, Odp_Klucz_t] | None = None):
        self.ID: UUID_Test_t = ID
        
        self.zamkniety: bool = False
        self.pytania: dict[ID_Pytanie_t, Pytanie] = pytania
        self.pytanie_na_arkusz: int = pytania_na_arkusz
        self.klucz_odp: Odp_Klucz_t = klucz_odp
        
        self.uczesticy: dict[UUID_Urzytkownik_t, Odp_Klucz_t] = uczestnicy if uczestnicy else {}
    
    def losowy_arkusz(self, uczen: User) -> ArkuszResponse:
        if uczen.typ != UzytkonikTyp.UCZEN:
            raise ValueError("Zły typ urzytkownika.", 
                             f"wymagano: {UzytkonikTyp.UCZEN}",
                             f"Otrzymano: {uczen.typ}")
            
        self.uczesticy[uczen.ID] = {}
        uczen.testy.append(self.ID)
        
        pytania: list[Pytanie] = sample(list(self.pytania.values()), k=self.pytanie_na_arkusz)
        pytania_response: list[PytanieResponse] = []
        
        for pytanie in pytania:
            pytanie.odp = sample(pytanie.odp, k=len(pytanie.odp))
            pytania_response.append(PytanieResponse(ID=pytanie.ID, tresc=pytanie.tresc, odp=pytanie.odp))
        
        return ArkuszResponse(pytania=pytania_response)
    
    def odp_uzytkownika(self, uczen: User, odp: Odp_Klucz_t) -> None:
        if uczen.ID not in self.uczesticy:
            raise ValueError("Podany użytkonik nie jest przypisany do tego testu", f"test_id: {self.ID}",
                             f"Testy do których użytkownik o id: {uczen.ID}", f"uczen_test: {uczen.testy}")
        
        self.uczesticy[uczen.ID] = odp
        
        
class TestMenadzer:
    POPRAWNA_ODP: ID_Odp_t = 0
    def __init__(self):
        self.slownik_testow: dict[UUID_Test_t, Test] = {}
                
    def _add(self, test: Test) -> None:
        if test.ID in self.slownik_testow.keys():
            raise ValueError("Test o podanym ID już istnieje",
                             f"ID: {test.ID}")
        
        self.slownik_testow[test.ID] = test
        
    def stworz_test(self, pytania_na_arkusz: int, plik: PlikMenadzer) -> UUID_Test_t:
        test_ID: UUID_Test_t = uuid4().hex
        pytania: dict[ID_Pytanie_t, Pytanie] = {}
        klucz_odp: Odp_Klucz_t = {}
        
        for tresc, *odpowiedzi in plik.decode():
            pytanie_ID: ID_Pytanie_t = len(pytania)
            odpowiedz_praw: Odp_t = odpowiedzi[self.POPRAWNA_ODP]
            pytanie = Pytanie(ID=pytanie_ID, tresc=tresc, odp=odpowiedzi, odp_praw=odpowiedz_praw)
            
            pytania[pytanie_ID] = pytanie
            klucz_odp[pytanie_ID] = odpowiedz_praw
            
        if len(pytania) < pytania_na_arkusz:
            raise ValueError("Ilość pytań na arkusz jest większa od ilości dostępnych pytań", 
                             f"Ilość dostępnych pytań: {len(pytania)}",
                             f"Żądana ilość pytań: {pytania_na_arkusz}")
        
        test: Test = Test(ID=test_ID, pytania_na_arkusz=pytania_na_arkusz, 
                          pytania=pytania, klucz_odp=klucz_odp)
        self._add(test=test)
        
        return test_ID
    
    def get(self, ID: UUID_Test_t) -> Test:
        test: Test = self.slownik_testow.get(ID)
        
        if not test:
            raise ValueError("Nie znaleniono testu",
                             f"ID: {ID}")
        
        return test
        