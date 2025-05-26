from fastapi import status, HTTPException
from random import sample

# Pliki lokalne
from datamodel import (UUID_Test_t, ID_Pytanie_t, 
                       Odp_Punkty_t, Odp_t, Odp_Klucz_t, 
                       TestInfoResponse, Test_Status_t, TestWynikResponse, ArkuszResponse, 
                       PytanieResponse, UczenResponse, UczenWynikResponse)
from entitys.question_entity import Pytanie
from entitys.participant_entity import Uczestnik
from callback_register import CallbackRegister

class Test:
    def __init__(self, ID: UUID_Test_t,
                 pytania_na_arkusz: int,
                 pytania: dict[ID_Pytanie_t, Pytanie],
                 klucz_odp: Odp_Klucz_t,
                 callbackRegister: CallbackRegister | None = None) -> None:
        self._ID: UUID_Test_t = ID
        self._callbackRegister: CallbackRegister = callbackRegister if callbackRegister is not None else CallbackRegister()

        self._zamkniety: Test_Status_t = False
        self._pytania: dict[ID_Pytanie_t, Pytanie] = pytania
        self._pytania_na_arkusz: int = pytania_na_arkusz
        self._klucz_odp: Odp_Klucz_t = klucz_odp
        
        self._uczestnicy: list[Uczestnik] = []

    @property
    def ID(self) -> UUID_Test_t:
        return self._ID
    
    @property
    def zamkniety(self) -> Test_Status_t:
        return self._zamkniety
    
    @property
    def callbackRegister(self) -> CallbackRegister:
        return self._callbackRegister 
    
    @property
    def wyniki(self) -> list[UczenWynikResponse]:
        return [UczenWynikResponse(klucz_odp=_uczestnik.odpowiedzi, 
                                   uczen=UczenResponse(imie=_uczestnik.imie, nazwisko=_uczestnik.nazwisko),
                                   wynik=TestWynikResponse(punkty=_uczestnik.punkty, pytania_bledne=_uczestnik.pytania_blende)) 
                for _uczestnik in self._uczestnicy]  
    
    @property    
    def info(self) -> TestInfoResponse:
        return TestInfoResponse(ID=self._ID, zamkniety=self._zamkniety, 
                                pytania=[PytanieResponse(ID=pytanie.ID, tresc=pytanie.tresc, odp=pytanie.odp) for pytanie in self._pytania.values()], 
                                pytania_na_arkusz=self._pytania_na_arkusz,
                                klucz_odp=self._klucz_odp, 
                                uczestnicy_odpowiedzi=self.wyniki)
    
    def __str__(self) -> str:
        return (f"Test(ID={self._ID}, zamkniety={self._zamkniety}")
    
    def zamknij(self) -> list[UczenWynikResponse]:
        self._zamkniety = True
        
        return self.wyniki
    
    def losowy_arkusz(self) -> ArkuszResponse:
        if self._zamkniety:
            raise ValueError("Test został juz zakońcony")
        
        pytania: list[Pytanie] = sample(list(self._pytania.values()), k=self._pytania_na_arkusz)
        pytania_response: list[PytanieResponse] = []
        
        for pytanie in pytania:
            pytanie.odp = sample(pytanie.odp, k=len(pytanie.odp))
            pytania_response.append(PytanieResponse(ID=pytanie.ID, tresc=pytanie.tresc, odp=pytanie.odp))
        
        return ArkuszResponse(pytania=pytania_response)
    
    def odp_spraw(self, odp: Odp_Klucz_t) -> TestWynikResponse:
        punkty: Odp_Punkty_t = 0
        pytania_bledne: list[ID_Pytanie_t] = []
        
        for pytanie_id, odp_ucznia in odp.items():
            try:
                odp_praw: Odp_t = self._pytania[pytanie_id].odp_praw
            except KeyError:
                raise ValueError("Pytanie o podanym id nie istnieje", 
                                 f"ID: {pytanie_id}")
                
            if odp_praw == odp_ucznia:
                punkty += 1
            else:
                pytania_bledne.append(pytanie_id)
                
        return TestWynikResponse(punkty=punkty, pytania_bledne=sorted(pytania_bledne))
    
    def odp_uzytkownika(self, uczestnik: Uczestnik) -> TestWynikResponse:
        if self._zamkniety:
            raise ValueError("Test został juz zakońcony")
        elif len(uczestnik.odpowiedzi) < self._pytania_na_arkusz:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=["Nie przesłano wszystkich pytań", 
                             f"otzymano: {len(uczestnik.odpowiedzi)}", f"oczekiwano: {self._pytania_na_arkusz}"])
        elif len(uczestnik.odpowiedzi) > self._pytania_na_arkusz:
            raise ValueError("Przesłano za dużo pytań", 
                             f"otzymano: {len(uczestnik.odpowiedzi)}", f"oczekiwano: {self._pytania_na_arkusz}")
        
        wynik: TestWynikResponse = self.odp_spraw(odp=uczestnik.odpowiedzi)
        uczestnik.punkty = wynik.punkty
        uczestnik.pytania_blende = wynik.pytania_bledne
        
        self._uczestnicy.append(uczestnik)
        self._callbackRegister.powiadom(self.info)
        
        return wynik
      