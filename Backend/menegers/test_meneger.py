from __future__ import annotations
from uuid import uuid4

# Lokalne pliki
from datamodel import (ID_Odp_t, ID_Pytanie_t, TestStworzonyResponse, UUID_Test_t, Odp_Klucz_t, Odp_t)
from entitys.file_entity import PlikEncDecCSV
from entitys.test_entity import Test
from entitys.question_entity import Pytanie

#!: Singleton 
class TestMenadzer:
    POPRAWNA_ODP: ID_Odp_t = 0
    def __init__(self):
        self.slownik_testow: dict[UUID_Test_t, Test] = {}
                
    def __new__(cls, *args, **kwargs):
        if "_obiekt" not in cls.__dict__:
            cls._obiekt = super().__new__(cls, *args, **kwargs)
        return cls._obiekt
    
    def _add(self, test: Test) -> None:
        if test.ID in self.slownik_testow.keys():
            raise ValueError("Test o podanym ID już istnieje",
                             f"ID: {test.ID}")
        
        self.slownik_testow[test.ID] = test
        
    def get(self, ID: UUID_Test_t) -> Test:
        try:
            test: Test = self.slownik_testow[ID]
        except KeyError:
            raise ValueError("Nie znaleniono testu",
                             f"ID: {ID}")
        
        return test
    
    def dostepne_testy(self, zamkniete: bool) -> list[TestStworzonyResponse]:
        return [TestStworzonyResponse(test_id=test_id) for test_id, test in self.slownik_testow.items() if not test.zamkniety or zamkniete]
    
    def stworz_test(self, pytania_na_arkusz: int, plik: PlikEncDecCSV) -> UUID_Test_t:
        test_ID: UUID_Test_t = uuid4().hex
        pytania: dict[ID_Pytanie_t, Pytanie] = {}
        klucz_odp: Odp_Klucz_t = {}
        
        for tresc, *odpowiedzi in plik.decode():
            pytanie_ID: ID_Pytanie_t = len(pytania) + 1
            
            if len(odpowiedzi) != 4:
                raise ValueError("Niepoprawna ilość odpowiedzi w pytaniu",
                                 f"ID pytania: {pytanie_ID}",
                                 f"Treść pytania: {tresc}",
                                 f"Ilość odpowiedzi: {len(odpowiedzi)}",
                                 "Oczekiwano 4 odpowiedzi")
            
            odpowiedz_praw: Odp_t = odpowiedzi[self.POPRAWNA_ODP]
            pytanie = Pytanie(ID=pytanie_ID, tresc=tresc, odp=odpowiedzi, odp_praw=odpowiedz_praw)
            
            pytania[pytanie_ID] = pytanie
            klucz_odp[pytanie_ID] = odpowiedz_praw
            
        if len(pytania) < pytania_na_arkusz:
            raise  ValueError("Ilość pytań na arkusz jest większa od ilości dostępnych pytań", 
                             f"Ilość dostępnych pytań: {len(pytania)}",
                             f"Żądana ilość pytań: {pytania_na_arkusz}")
        
        test: Test = Test(ID=test_ID, pytania_na_arkusz=pytania_na_arkusz, 
                          pytania=pytania, klucz_odp=klucz_odp)
        self._add(test=test)
        
        return test_ID   
 
TEST_MENADZER: TestMenadzer = TestMenadzer()