import asyncio
from typing import Annotated
from fastapi import APIRouter, Body, Path, UploadFile, WebSocket, WebSocketDisconnect, status, File


# Pliki lokalne
from datamodel import TestInfoResponse, TestStworzonyResponse, UUID_Test_t, UczenWynikResponse
from httperror import HTTP_Value_Exception
# from entitys.watcher_entity import ObserwatorWynikow
from menegers.file_meneger import Plik, PlikMenadzer
from menegers.test_meneger import TEST_MENADZER, Test



ROUTER_NAUCZYCZIEL = APIRouter()

@ROUTER_NAUCZYCZIEL.get(path="/test/",
         name="Dostępne testy",
         description="Lista wszytkich dostępnych dla nauczyciela testów\
             \nW tym rózwnież zamkniete testy",
         status_code=status.HTTP_200_OK,
         response_model=list[TestStworzonyResponse])
def test_wszystkie():
    #TODO: Do poprawy
    return TEST_MENADZER.dostepne_testy(zamkniete=True)

@ROUTER_NAUCZYCZIEL.post(path="/test/stworz",
          name="Stwórz test",
          description="Tworzenie testu",
          status_code=status.HTTP_201_CREATED,
          response_model=TestStworzonyResponse,
          response_description="Id utworzonego testu",
          operation_id="Stwórz test")
def test_stworz(liczba_pytan: Annotated[int, Body(title="Liczba pytanń",
                                                  description="Ilość pytań przypadającza na arkusz - Dla ucznia\
                                                      \nNie określa ilości pytań w pliku.\
                                                      \nNie może być większe niż ilość pytań w pliku csv",
                                                  ge=1)], 
                plik_csv: Annotated[UploadFile, File(title="Plik csv", 
                                                     description="Plik z pytaniami w formacie csv")],
                plik_zapisac: Annotated[bool, Body(title="Plik zapisac", 
                                                   description="Wartość deczydującza czy plik zostanie zapisany na serwerze")] = None):
    try:
        with PlikMenadzer() as PM:
            plik_csv: Plik = PM.UploadFile(plik_csv, zapisac=plik_zapisac if plik_zapisac else False)
            test_id: UUID_Test_t = TEST_MENADZER.stworz_test(liczba_pytan, plik_csv)
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)
    
    return TestStworzonyResponse(test_id=test_id)

@ROUTER_NAUCZYCZIEL.get(path="/test/{test_id}/info",
         name="Informacje o teście",
         description="Informacje o teście",
         status_code=status.HTTP_200_OK,
         response_model=TestInfoResponse,
         response_description="Informacje o teście")
def test_info(test_id: Annotated[UUID_Test_t, Path()]) -> TestInfoResponse:
    try: 
        test: Test = TEST_MENADZER.get(test_id)
        return test.info()
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
        return test.get_uczestnicy_response()
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
        return test.zamknij()
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)    

#TODO: Do poprawy
@ROUTER_NAUCZYCZIEL.websocket("/test/{test_id}/info/ws")
async def test(test_id: UUID_Test_t, websocket: WebSocket):
    try:
        test: Test = TEST_MENADZER.get(test_id)
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)
    
    await websocket.accept()
    while True:
        try:
            if not test.zamkniety:
                await websocket.send_json(test.info().model_dump())
            else:
                break
        except WebSocketDisconnect:
            pass
        await asyncio.sleep(1)
    await websocket.close()
        
#?: Dodać usuwanie testu