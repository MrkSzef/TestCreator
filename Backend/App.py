from __future__ import annotations
from fastapi import Body, FastAPI, File, Path, UploadFile, status
from typing import Annotated
import uvicorn

# Lokalne pliki
from httperror import HTTP_Value_Exception
from datamodel import (ArkuszResponse, Odp_Klucz_t, TestStworzonyResponse, UUID_Test_t, UUID_Urzytkownik_t, UserInfoResponse, imie, nazwisko, UzytkonikTyp , FastApiTags )
from meneger.test_meneger import Test, TestMenadzer
from meneger.user_meneger import User, UserMenadzer
from meneger.file_meneger import PlikMenadzer

# Zmiene globalne
TEST_MENADZER: TestMenadzer = TestMenadzer()
USER_MENADZER: UserMenadzer = UserMenadzer()

# FastApi
# Opis tagów
TAGS_METADATA = [
    {
        "name": FastApiTags.NAUCZYCIEL,
        "description": "Tworzenie testów oraz ich kontrolowanie"
    },
    {
        "name": FastApiTags.UCZEN,
        "description": "Pobieranie arkuszy oraz wysyłanie odpowiedz"
    },
    {
        "name": FastApiTags.UZYTKOWNIK,
        "description": "Zarządzanie użytkownikami"
    },
]
# Aplikacja
APP = FastAPI(title="TestCreator API",
              description="API służącze do przeprowadzania testów",
              version="0.0.3",
              openapi_tags=TAGS_METADATA)

# Nauczyciel
@APP.post(path="/nauczyciel/test/stworz",
          name="Stwórz test",
          status_code=status.HTTP_201_CREATED,
          tags=[FastApiTags.NAUCZYCIEL],
          response_model=TestStworzonyResponse,
          response_description="Id utworzonego testu",
          operation_id="Stwórz test")
def stworz_test(liczba_pytan: Annotated[int, Body(title="Liczba pytanń",
                                                  description="Ilość pytań przypadającza na arkusz")], 
                plik_csv: Annotated[UploadFile, File(title="Plik csv", 
                                                     description="Plik z pytaniami w formacie csv")]):
    plik_csv: PlikMenadzer = PlikMenadzer(plik_csv)
    
    try:
        test_id: UUID_Test_t = TEST_MENADZER.stworz_test(liczba_pytan, plik_csv)
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)
    
    return TestStworzonyResponse(test_id=test_id)

# Uczeń
@APP.get(path="/uczen/arkusz/{test_id}", 
         name="Losowy arkusz",
         status_code=status.HTTP_200_OK, 
         tags=[FastApiTags.UCZEN],
         response_model=ArkuszResponse,
         response_description="Arkusz z pytaniami")
def losowy_arkusz(test_id: Annotated[UUID_Test_t, Path()], 
                  uczen_id: Annotated[UUID_Urzytkownik_t, Body()]) -> ArkuszResponse:
    try:
        uczen: User = USER_MENADZER.get(uczen_id)
        test: Test = TEST_MENADZER.get(test_id)
        arkusz: ArkuszResponse = test.losowy_arkusz(uczen=uczen)
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)
    
    return arkusz


# Wysyłać wyniki jako odpowiedz ???
@APP.post(path="/uczen/arkusz/{test_id}/odaji", 
          name="Wyślij odpowiedzi",
          status_code=status.HTTP_200_OK,
          tags=[FastApiTags.UCZEN],
          operation_id="Wyślji odpowiedzi")
def wyslij_odp(test_id: Annotated[UUID_Test_t, Path()],
               uczen_id: Annotated[UUID_Urzytkownik_t, Body()],
               odp: Annotated[Odp_Klucz_t, Body()]):
    try:
        uczen: User = USER_MENADZER.get(uczen_id)
        test: Test = TEST_MENADZER.get(test_id)
        
        test.odp_uzytkownika(uczen=uczen, odp=odp)
        
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)


# Użytkownicy
@APP.post(path="/urzytkownicy/stworz", 
          name="Stwórz użytkownika",
          status_code=status.HTTP_201_CREATED,
          tags=[FastApiTags.UZYTKOWNIK],
          response_model=UUID_Urzytkownik_t,
          response_description="ID utworzonego użytkownika",
          operation_id="Utwórz użytkownika")
def stworz_uzytkownika(imie: Annotated[imie, Body()],
                        nazwisko: Annotated[nazwisko, Body()],
                        typ_uzytkownika: Annotated[UzytkonikTyp, Body()] = None) -> UUID_Urzytkownik_t:
    if not typ_uzytkownika:
        typ_uzytkownika = UzytkonikTyp.UCZEN
    try: 
        uztkownik_id: UUID_Test_t = USER_MENADZER.stworz_uzytkownika(imie=imie, nazwisko=nazwisko, typ=typ_uzytkownika)
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)
    
    return uztkownik_id  
    
@APP.get(path="/urzytkownicy/{uzytkownik_id}", 
          name="Użytkownik",
          status_code=status.HTTP_200_OK,
          tags=[FastApiTags.UZYTKOWNIK],
          response_model=UserInfoResponse,
          response_description="Informacje o użytkowniku")
def uzytkownik(uzytkownik_id: Annotated[UUID_Urzytkownik_t, Path()]) -> UserInfoResponse:
    try:
        uzytkownik: User = USER_MENADZER.get(uzytkownik_id)
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)
    
    return UserInfoResponse(ID=uzytkownik.ID,
                            typ=uzytkownik.typ,
                            imie=uzytkownik.imie,
                            nazwisko=uzytkownik.nazwisko,
                            testy=uzytkownik.testy)
    
"""  Endpointy do dodania
@APP.post(path="/urzytkownicy/{urztkownik_id}/usun", status_code=status.HTTP_200_OK)   
@APP.get("/nauczyciel/test/{test_id}/zamknij", status_code=status.HTTP_200_OK)
@APP.get("/nauczyciel/test/{test_id}", status_code=status.HTTP_200_OK)
"""

if __name__ == "__main__":
    uvicorn.run(app="App:APP", host="0.0.0.0", port=8000, reload=False)
