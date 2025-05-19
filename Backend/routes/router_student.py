from typing import Annotated
from fastapi import APIRouter, Body, Path, status

# Lokalne pliki
from datamodel import ArkuszResponse, Odp_Klucz_t, Test_Status_t, TestStworzonyResponse, TestWynikResponse, UUID_Test_t, imie_t, nazwisko_t, Uczen
from httperror import HTTP_Value_Exception
from menegers.test_meneger import TEST_MENADZER, Test

ROUTER_UCZEN: APIRouter = APIRouter()

@ROUTER_UCZEN.get(path="/test/",
         name="Dostępne testy",
         description="Lista dostępnycg testów dla ucznia.\
             \n Nie wyświetla zamknietych testów",
         status_code=status.HTTP_200_OK,
         response_model=list[TestStworzonyResponse])
def test_wszystkie():
    #TODO: Do poprawy
    return TEST_MENADZER.dostepne_testy_uczen()

@ROUTER_UCZEN.get(path="/test/{test_id}/zamkniety",
                  name="Test zamknięty ?",
                  description="Sprawdza czy test o podanym id jest zamkniety",
                  status_code=status.HTTP_200_OK,
                  response_model=bool,
                  response_description="Wartoćś bool oznaczającza czy dany test jest zamknięty\
                      \nTreu - Test zamkniety\nFalse - Test otwary",
                  operation_id="Status testu")
def test_otwarty(test_id: Annotated[UUID_Test_t, Path()]):
    try:
        test: Test = TEST_MENADZER.get(test_id)
        test_status: Test_Status_t = test.zamkniety
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)
    
    return test_status


@ROUTER_UCZEN.get(path="/arkusz/{test_id}", 
         name="Losowy arkusz",
         status_code=status.HTTP_200_OK, 
         description="Pobieranie arkusza z losowo wybranymi pytaniami",
         response_model=ArkuszResponse,
         response_description="Arkusz z pytaniami")
def losowy_arkusz(test_id: Annotated[UUID_Test_t, Path()]) -> ArkuszResponse:
    try:
        test: Test = TEST_MENADZER.get(test_id)
        arkusz: ArkuszResponse = test.losowy_arkusz()
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)
    
    return arkusz

@ROUTER_UCZEN.post(path="/arkusz/{test_id}/odaji", 
          name="Wyślij odpowiedzi",
          description="Wysyłanie odpowiedzi na serwer\
              \n!!! UWAGA !!! - Kluczem w odp jest id pytania.",
          status_code=status.HTTP_200_OK,
          response_model=TestWynikResponse,
          response_description="Uzyskany wynik",
          operation_id="Wyslji odpowiedzi",)
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
