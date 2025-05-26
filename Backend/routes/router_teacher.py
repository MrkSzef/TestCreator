from __future__ import annotations
from typing import Annotated, cast
from fastapi import APIRouter, Body, Path, UploadFile, WebSocket, WebSocketDisconnect, status, File
from asyncio import Queue
from pydantic import BaseModel

# Pliki lokalne
from datamodel import TestInfoResponse, TestStworzonyResponse, UUID_Test_t, UczenWynikResponse
from httperror import HTTP_Value_Exception
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
                plik_zapisac: Annotated[bool | None, Body(title="Plik zapisac", 
                                                   description="Wartość deczydującza czy plik zostanie zapisany na serwerze")] = None):
    try:
        with PlikMenadzer() as PM:
            plik: PlikEncDecCSV = PM.stworz(plik_csv.file, plik_nazwa=plik_csv.filename, 
                                            zapisac=bool(plik_zapisac) if None not in (plik_zapisac, plik_csv.filename) else False)
            test_id: UUID_Test_t = TEST_MENADZER.stworz_test(liczba_pytan, plik)
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
        return test.info
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
        return test.wyniki
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
async def test_info_ws(test_id: UUID_Test_t, websocket: WebSocket):
    try:
        test: Test = TEST_MENADZER.get(test_id)
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)
    
    await websocket.accept()
    que: Queue = Queue(maxsize=5)
    test_info_callback: InfoCallback = InfoCallback(que=que)
    test.callbackRegister.subskrybuj(test_info_callback)
    try:
        while True:
            test_info: TestInfoResponse = cast(TestInfoResponse, await que.get())
            await websocket.send_json(test_info.model_dump())
    except WebSocketDisconnect:
        print(f"WebSocket powiazany z testem: {test_id} \nzostał rozłączony")
    finally:
        await websocket.close()        
        test.callbackRegister.odsubskrybuj(test_info_callback)

#TODO: Do poprawy
@ROUTER_NAUCZYCZIEL.websocket("/test/{test_id}/wyniki/ws")
async def test_wyniki_ws(test_id: UUID_Test_t, websocket: WebSocket):
    try:
        test: Test = TEST_MENADZER.get(test_id)
    except ValueError as e:
        raise HTTP_Value_Exception(e.args)
    
    await websocket.accept()
    que: Queue = Queue(maxsize=5)
    test_wuniki_callback: WynikCallback = WynikCallback(que=que)
    test.callbackRegister.subskrybuj(test_wuniki_callback)
    try:
        while True:
            test_wyniki: list[UczenWynikResponse] = cast(list[UczenWynikResponse], await que.get())
            await websocket.send_json([cast(BaseModel, model).model_dump() for model in test_wyniki])
    finally:
        await websocket.close()        
        test.callbackRegister.odsubskrybuj(test_wuniki_callback)
#?: Dodać usuwanie testu