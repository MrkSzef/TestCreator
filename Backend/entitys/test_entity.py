from fastapi import status, HTTPException
from random import sample

# Pliki lokalne
from datamodel import (UUID_Test_t, ID_Pytanie_t, 
                       Odp_Punkty_t, Odp_t, Odp_Klucz_t, 
                       TestInfoResponse, Test_Status_t, TestWynikResponse, ArkuszResponse, 
                       PytanieResponse, UczenResponse, UczenWynikResponse)
from entitys.question_entity import Pytanie
from entitys.participant_entity import Uczestnik

class Test:
    def __init__(self, ID: UUID_Test_t,
                 pytania_na_arkusz: int,
                 pytania: dict[ID_Pytanie_t, Pytanie],
                 klucz_odp: Odp_Klucz_t):
        self.ID: UUID_Test_t = ID

        self.zamkniety: Test_Status_t = False
        self.pytania: dict[ID_Pytanie_t, Pytanie] = pytania
        self.pytania_na_arkusz: int = pytania_na_arkusz
        self.klucz_odp: Odp_Klucz_t = klucz_odp
        
        self.uczestnicy: list[Uczestnik] = []

    def get_uczestnicy_response(self) -> list[UczenWynikResponse]:
        return [UczenWynikResponse(klucz_odp=_uczestnik.odpowiedzi, 
                                   uczen=UczenResponse(imie=_uczestnik.imie, nazwisko=_uczestnik.nazwisko),
                                   wynik=TestWynikResponse(punkty=_uczestnik.punkty, pytania_bledne=_uczestnik.pytania_blende)) 
                for _uczestnik in self.uczestnicy]
        
    def info(self) -> TestInfoResponse:
        return TestInfoResponse(ID=self.ID, zamkniety=self.zamkniety, 
                                pytania=[PytanieResponse(ID=pytanie.ID, tresc=pytanie.tresc, odp=pytanie.odp) for pytanie in self.pytania.values()], 
                                pytania_na_arkusz=self.pytania_na_arkusz,
                                klucz_odp=self.klucz_odp, 
                                uczestnicy_odpowiedzi=self.get_uczestnicy_response())
    
    def zamknij(self) -> list[UczenWynikResponse]:
        self.zamkniety = True
        
        return self.get_uczestnicy_response()
    
    def losowy_arkusz(self) -> ArkuszResponse:
        if self.zamkniety:
            raise ValueError("Test został juz zakońcony")
        
        pytania: list[Pytanie] = sample(list(self.pytania.values()), k=self.pytania_na_arkusz)
        pytania_response: list[PytanieResponse] = []
        
        for pytanie in pytania:
            pytanie.odp = sample(pytanie.odp, k=len(pytanie.odp))
            pytania_response.append(PytanieResponse(ID=pytanie.ID, tresc=pytanie.tresc, odp=pytanie.odp))
        
        return ArkuszResponse(pytania=pytania_response)
    
    def odp_spraw(self, odp: Odp_Klucz_t) -> TestWynikResponse:
        punkty: Odp_Punkty_t = 0
        pytania_bledne: list[ID_Pytanie_t] = []
        
        for pytanie_id, odp_ucznia in odp.items():
            odp_praw: Odp_t = self.pytania.get(pytanie_id).odp_praw
            if not odp_praw:
                raise ValueError("Pytanie o podanym id nie istnieje", 
                                 f"ID: {pytanie_id}")
                
            if odp_praw == odp_ucznia:
                punkty += 1
            else:
                pytania_bledne.append(pytanie_id)
                
        return TestWynikResponse(punkty=punkty, pytania_bledne=sorted(pytania_bledne))
    
    def odp_uzytkownika(self, uczestnik: Uczestnik) -> TestWynikResponse:
        if self.zamkniety:
            raise ValueError("Test został juz zakońcony")
        elif len(uczestnik.odpowiedzi) < self.pytania_na_arkusz:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=["Nie przesłano wszystkich pytań", 
                             f"otzymano: {len(uczestnik.odpowiedzi)}", f"oczekiwano: {self.pytania_na_arkusz}"])
        elif len(uczestnik.odpowiedzi) > self.pytania_na_arkusz:
            raise ValueError("Przesłano za dużo pytań", 
                             f"otzymano: {len(uczestnik.odpowiedzi)}", f"oczekiwano: {self.pytania_na_arkusz}")
        
        wynik: TestWynikResponse = self.odp_spraw(odp=uczestnik.odpowiedzi)
        uczestnik.punkty = wynik.punkty
        uczestnik.pytania_blende = wynik.pytania_bledne
        
        self.uczestnicy.append(uczestnik)
        
        return wynik
      