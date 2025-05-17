from __future__ import annotations
from fastapi import Body, FastAPI, File, Path, UploadFile, status
from fastapi.encoders import jsonable_encoder
from typing import Annotated
import uvicorn

# Lokalne pliki
from httperror import HTTP_Value_Exception
from datamodel import (ArkuszResponse, Odp_Klucz_t,
                       TestStworzonyResponse, TestWynikResponse, TestZamknietyResponse, UUID_Test_t,
                       UUID_Urzytkownik_t, FastApiTags, Uczen,
                       imie_t, nazwisko_t)
from meneger.test_meneger import Test, TestMenadzer
from meneger.file_meneger import PlikMenadzer

# Zmiene globalne
TEST_MENADZER: TestMenadzer = TestMenadzer()

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
def test_stworz(liczba_pytan: Annotated[int, Body(title="Liczba pytanń",
                                                  description="Ilość pytań przypadającza na arkusz")], 
                plik_csv: Annotated[UploadFile, File(title="Plik csv", 
                                                     description="Plik z pytaniami w formacie csv")]):
    plik_csv: PlikMenadzer = PlikMenadzer(plik_csv)
    
    try:
        test_id: UUID_Test_t = TEST_MENADZER.stworz_test(liczba_pytan, plik_csv)
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)
    
    return TestStworzonyResponse(test_id=test_id)

@APP.get(path="/nauczyciel/test/{test_id}/zamknij", 
         name="Zamknij test",
         status_code=status.HTTP_200_OK,
         tags=[FastApiTags.NAUCZYCIEL],
         response_model=TestZamknietyResponse)
def test_zamknij(test_id: UUID_Test_t) -> TestZamknietyResponse:
    try:
        test: Test = TEST_MENADZER.get(test_id)
        wyniki = test.zamknij()
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)    
    
    return wyniki

# Uczeń
@APP.get(path="/uczen/arkusz/{test_id}", 
         name="Losowy arkusz",
         status_code=status.HTTP_200_OK, 
         tags=[FastApiTags.UCZEN],
         response_model=ArkuszResponse,
         response_description="Arkusz z pytaniami")
def losowy_arkusz(test_id: Annotated[UUID_Test_t, Path()]) -> ArkuszResponse:
    try:
        test: Test = TEST_MENADZER.get(test_id)
        arkusz: ArkuszResponse = test.losowy_arkusz()
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)
    
    return arkusz

@APP.post(path="/uczen/arkusz/{test_id}/odaji", 
          name="Wyślij odpowiedzi",
          status_code=status.HTTP_200_OK,
          tags=[FastApiTags.UCZEN],
          response_model=TestWynikResponse,
          response_description="Uzyskany wynik",
          operation_id="Wyślji odpowiedzi",)
def wyslij_odp(test_id: Annotated[UUID_Test_t, Path()],
               imie: Annotated[imie_t, Body()],
               nazwisko: Annotated[nazwisko_t, Body()],
               odp: Annotated[Odp_Klucz_t, Body()]):
    try:
        uczen: Uczen = Uczen(imie=imie, nazwisko=nazwisko)
        test: Test = TEST_MENADZER.get(test_id)
        
        wynik: TestWynikResponse = test.odp_uzytkownika(uczen=uczen, odp=odp)
        
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)
    
    return wynik

if __name__ == "__main__":
    uvicorn.run(app="App:APP", host="0.0.0.0", port=8000, reload=False)
