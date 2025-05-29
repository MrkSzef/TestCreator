from __future__ import annotations
from typing import Annotated
from fastapi import APIRouter, Body, Path, UploadFile, WebSocket, status, File

# Pliki lokalne
from callback_register import CallbackRegister
from datamodel import Plik_Nazwa_t, TestInfoResponse, TestStworzonyResponse, UUID_Test_t, UczenWynikResponse
from httperror import HTTP_Value_Exception
from notification import PowiadomieniaWebsocket
from entitys.test_entity import Test
from entitys.callback_entity import InfoCallback, WynikCallback
from menegers.file_meneger import PlikMenadzer, PlikEncDecCSV
from menegers.test_meneger import TEST_MENADZER


ROUTER_NAUCZYCZIEL = APIRouter()

@ROUTER_NAUCZYCZIEL.get(path="/test/",
         name="Dostępne testy",
         description="Lista wszytkich dostępnych dla nauczyciela testów\
             \nW tym rózwnież zamkniete testy",
         status_code=status.HTTP_200_OK,
         response_model=list[TestStworzonyResponse])
def test_wszystkie() -> list[TestStworzonyResponse]:
    #TODO: Do poprawy
    return TEST_MENADZER.dostepne_testy(zamkniete=True)

@ROUTER_NAUCZYCZIEL.post(path="/test/stworz",
          name="Stwórz test",
          description="Tworzenie testu\n\
              Tworzenie testu z pliku csv przesłanego w body",
          status_code=status.HTTP_201_CREATED,
          response_model=TestStworzonyResponse,
          response_description="Id utworzonego testu",
          operation_id="Stwórz test POST")
def test_stworz_post(liczba_pytan: Annotated[int, Body(title="Liczba pytanń",
                                                  description="Ilość pytań przypadającza na arkusz - Dla ucznia\
                                                      \nNie określa ilości pytań w pliku.\
                                                      \nNie może być większe niż ilość pytań w pliku csv",
                                                  ge=1)], 
                plik_csv: Annotated[UploadFile, File(title="Plik csv", 
                                                     description="Plik z pytaniami w formacie csv")],
                plik_zapisac: Annotated[bool, Body(title="Plik zapisac", 
                                                   description="Wartość deczydującza czy plik zostanie zapisany na serwerze")] = False):
    try:
        with PlikMenadzer() as PM:
            plik: PlikEncDecCSV = PM.stworz(plik_csv.file, plik_nazwa=plik_csv.filename, 
                                            zapisac=plik_zapisac)
            test_id: UUID_Test_t = TEST_MENADZER.stworz_test(liczba_pytan, plik)
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)
    
    return TestStworzonyResponse(test_id=test_id)

@ROUTER_NAUCZYCZIEL.get(path="/test/stworz",
          name="Stwórz test",
          description="Tworzenie testu\n\
              Tworzenie testu z pliku csv znajdującego się na serwerze",
          status_code=status.HTTP_201_CREATED,
          response_model=TestStworzonyResponse,
          response_description="Id utworzonego testu",
          operation_id="Stwórz test GET")
def test_stworz_get(liczba_pytan: Annotated[int, Body(title="Liczba pytanń",
                                                  description="Ilość pytań przypadającza na arkusz - Dla ucznia\
                                                      \nNie określa ilości pytań w pliku.\
                                                      \nNie może być większe niż ilość pytań w pliku csv",
                                                  ge=1)], 
                plik_csv: Annotated[Plik_Nazwa_t, File(title="Plik csv", 
                                                     description="nazwa pliku zapisanego na serwerze")]) -> TestStworzonyResponse:
    try:
        with PlikMenadzer() as PM:
            plik: PlikEncDecCSV = PM.otworz(plik_nazwa=plik_csv)
            test_id: UUID_Test_t = TEST_MENADZER.stworz_test(liczba_pytan, plik)
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)
    
    return TestStworzonyResponse(test_id=test_id)

@ROUTER_NAUCZYCZIEL.delete(path="/test/{test_id}",
                           name="Usuń test",
                           description="Usuwanie testu",
                           status_code=status.HTTP_204_NO_CONTENT,
                           response_description="Test został usunięty")
def test_usun(test_id: Annotated[UUID_Test_t, Path()]): #!: -> None Powoduje bład 
    try:
        TEST_MENADZER.usun_test(test_id)
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)
    return None

@ROUTER_NAUCZYCZIEL.get(path="/test/{test_id}/info",
         name="Informacje o teście",
         description="Informacje o teście",
         status_code=status.HTTP_200_OK,
         response_model=TestInfoResponse,
         response_description="Informacje o teście")
def test_info(test_id: Annotated[UUID_Test_t, Path()]) -> TestInfoResponse:
    try: 
        test: Test = TEST_MENADZER.get(test_id)
        return test.getInfo()
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)

@ROUTER_NAUCZYCZIEL.get(path="/test/{test_id}/wyniki",
                        name="Wyniki uczniów",
                        description="Informacje o wynikach urzyskanych przez uczniów",
                        status_code=status.HTTP_200_OK,
                        response_model=list[UczenWynikResponse])
def test_wyniki(test_id: Annotated[UUID_Test_t, Path()]) -> list[UczenWynikResponse]:
    try:
        test: Test = TEST_MENADZER.get(test_id)
        return test.getWyniki()
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)

@ROUTER_NAUCZYCZIEL.get(path="/test/{test_id}/zamknij", 
         name="Zamknij test",
         description="Zamykanie testu.\
             \nBlokowanie ucznią możliwości pobierania losowego arkusz oraz wysyłania odpowiedzi",
         status_code=status.HTTP_200_OK,
         response_model=list[UczenWynikResponse])
def test_zamknij(test_id: Annotated[UUID_Test_t, Path()]) -> list[UczenWynikResponse]:
    try:
        test: Test = TEST_MENADZER.get(test_id)
        test.zamknij()
        return test.getWyniki()
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)    

@ROUTER_NAUCZYCZIEL.get(path="/test/{test_id}/otworz",
         name="Otwórz test",
         description="Otwieranie testu.\
             \nPozwala uczniom na pobieranie losowego arkusza oraz wysyłanie odpowiedzi",
         status_code=status.HTTP_200_OK,
         response_model=None)
def test_otworz(test_id: Annotated[UUID_Test_t, Path()]) -> None:
    try:
        test: Test = TEST_MENADZER.get(test_id)
        test.otworz()
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)

@ROUTER_NAUCZYCZIEL.get(path="/test/{test_id}/reset",
         name="Resetuj test",
         description="Resetowanie testu.\
             \nOtwiera test ponownie i usuwa wszystkie odpowiedzi uczniów",
         status_code=status.HTTP_204_NO_CONTENT)
def test_reset(test_id: Annotated[UUID_Test_t, Path()]): #!: -> None Powoduje bład 
    try:
        test: Test = TEST_MENADZER.get(test_id)
        test.reset()
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)
    return None

@ROUTER_NAUCZYCZIEL.websocket("/test/{test_id}/info/ws")
async def test_info_ws(test_id:  Annotated[UUID_Test_t, Path()], websocket: WebSocket):
    try:
        callbackregister: CallbackRegister = TEST_MENADZER.get(test_id).callbackRegister
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)
    
    async with PowiadomieniaWebsocket(websocket) as PW:
        callbackregister.subskrybuj(PW.stworz_callback(InfoCallback))
        await PW.start()
        
@ROUTER_NAUCZYCZIEL.websocket("/test/{test_id}/wyniki/ws")
async def test_wyniki_ws(test_id:  Annotated[UUID_Test_t, Path()], websocket: WebSocket):
    try:
        callbackregister: CallbackRegister = TEST_MENADZER.get(test_id).callbackRegister
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)
    
    async with PowiadomieniaWebsocket(websocket, que_size=10) as PW:
        callbackregister.subskrybuj(PW.stworz_callback(WynikCallback))
        await PW.start()