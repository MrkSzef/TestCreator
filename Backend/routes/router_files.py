from __future__ import annotations
from typing import Annotated
from fastapi import APIRouter, Body, File, Path, UploadFile
from fastapi import status
from fastapi.responses import FileResponse

# Pliki lokalne
from httperror import HTTP_Not_found
from datamodel import Plik_Nazwa_t
from menegers.file_meneger import PlikMenadzer

ROUTER_PLIKI = APIRouter()

@ROUTER_PLIKI.get(path="/",
                  name="Lista plików",
                  description="Lista plików znajdujących się na serwerze",
                  status_code=status.HTTP_200_OK,
                  response_model=list[str],
                  response_description="Lista plików")
def pliki_lista() -> list[str]:
    return PlikMenadzer().lista()

@ROUTER_PLIKI.post(path="/",
                  name="Prześlij plik",
                  description="Przeszyłanie pliku na serwer",
                  status_code=status.HTTP_201_CREATED,
                  response_description="Plik został przesłany",
                  operation_id="Przeslij plik")
def plik_przeslij(plik: Annotated[UploadFile, File(title="Plik", description="Plik do przesłania na serwer")],
                  plik_nawza: Annotated[Plik_Nazwa_t, Body()]) -> None:
    with PlikMenadzer() as PM:
        PM.stworz(plik.file, 
                  plik_nazwa=plik_nawza, 
                  zapisac=True)
    return None

@ROUTER_PLIKI.get(path="/{plik_nazwa}",
                  name="Pobierz plik",
                  description="Pobieranie pliku znajdującego się na serwerze",
                  status_code=status.HTTP_200_OK,
                  response_description="Podany plik",
                  response_class=FileResponse)
def plik_pobierz(plik_nazwa: Annotated[Plik_Nazwa_t, Path()]) -> FileResponse:
    try:
        return FileResponse(**PlikMenadzer().pobierz(plik_nazwa))
    except ValueError as e:
        raise HTTP_Not_found(e.args)

@ROUTER_PLIKI.delete(path="/{plik_nazwa}",
                    name="Usuń plik",
                    description="Usuwanie pliku znajdującego się na serwerze",
                    status_code=status.HTTP_204_NO_CONTENT,
                    response_description="Plik został usunięty")
def plik_usun(plik_nazwa: Annotated[Plik_Nazwa_t, Path()]): #!: -> None Powoduje bład 
    try:
        PlikMenadzer().usun(plik_nazwa)
    except ValueError as e:
        raise HTTP_Not_found(e.args)
    return None