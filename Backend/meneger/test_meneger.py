from __future__ import annotations
from uuid import uuid4
from random import sample

# Lokalne pliki

from meneger.file_meneger import PlikMenadzer
from datamodel import (ID_Odp_t, ID_Pytanie_t, TestWynikResponse, TestZamknietyResponse,
                       UUID_Test_t, Odp_Klucz_t, Odp_lista_t, Odp_t,
                       PytanieResponse, ArkuszResponse, Uczen)

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
                 klucz_odp: Odp_Klucz_t):
        self.ID: UUID_Test_t = ID
        
        self.zamkniety: bool = False
        self.pytania: dict[ID_Pytanie_t, Pytanie] = pytania
        self.pytanie_na_arkusz: int = pytania_na_arkusz
        self.klucz_odp: Odp_Klucz_t = klucz_odp
        
        self.uczesticy: list[tuple[ Uczen, Odp_Klucz_t]] = []
    
    def zamknij(self) -> TestZamknietyResponse:
        self.zamkniety = True
        wyniki: list[tuple[Uczen, TestWynikResponse]] = []
        
        for uczen, odp in self.uczesticy:    
            wyniki.append((uczen, self.odp_spraw(odp=odp)))
        
        return TestZamknietyResponse(wyniki=wyniki)
    
    def losowy_arkusz(self) -> ArkuszResponse:
        if self.zamkniety:
            raise ValueError("Test został juz zakońcony")
        
        pytania: list[Pytanie] = sample(list(self.pytania.values()), k=self.pytanie_na_arkusz)
        pytania_response: list[PytanieResponse] = []
        
        for pytanie in pytania:
            pytanie.odp = sample(pytanie.odp, k=len(pytanie.odp))
            pytania_response.append(PytanieResponse(ID=pytanie.ID, tresc=pytanie.tresc, odp=pytanie.odp))
        
        return ArkuszResponse(pytania=pytania_response)
    
    def odp_spraw(self, odp: Odp_Klucz_t) -> TestWynikResponse:
        punkty: int = 0
        pytania_bledne: list[ID_Pytanie_t] = []
        
        for pytanie_id, odp_ucznia in odp.items():
            odp_praw: Odp_t = self.pytania.get(pytanie_id)
            if not odp_praw:
                raise ValueError("Pytanie o podanym id nie istnieje", 
                                 f"ID: {pytanie_id}")
                
            if odp_praw == odp_ucznia:
                punkty += 1
            else:
                pytania_bledne.append(pytanie_id)
                
        return TestWynikResponse(punkty=punkty, pytania_bledne=sorted(pytania_bledne))
    
    def odp_uzytkownika(self, uczen: Uczen, odp: Odp_Klucz_t) -> TestWynikResponse:
        if self.zamkniety:
            raise ValueError("Test został juz zakońcony")
        
        self.uczesticy.append((uczen, odp))
        
        return self.odp_spraw(odp=odp)
        
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
        