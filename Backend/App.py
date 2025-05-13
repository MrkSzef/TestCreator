from __future__ import annotations
from pydantic import BaseModel
from random import randint
import os
from fastapi import FastAPI
import json

# Aby uruchomić API należy wydać polecenie fastapi.exe dev .\App.py <-- Musi być uruchomiony tak nie .\Backend\App.py -- Bład sciećki
# Do zrobienia. Porawa funkji tworzenia testow oraz napisanie rzarzadania sciezka 
# Konfiguracja
FOLDER_PYTAN: str = "pliki_pytan" # Folder gdzie znajdują sie pliki z pytaniami
ZAKRES_T_ID: tuple[int, int] = (0, 9999) # Zakres w jakim będzie losowane id testu

#Globalne zmiene
app = FastAPI()
Lista_testow: dict[int : Test] = {} # type: ignore

class Pytanie(BaseModel):
    P_ID: int
    TEKST: str
    ODPOWIDZI: list[str]
    POPRAWNA: str

class Test(BaseModel):
    T_ID: int
    LISTA_PYTAN: list[Pytanie]
    
# Do dokonczenia
@app.get("/nauczyciel/stworz_test")
async def create_test(liczbaPytan: None = None, idPlikuCSV: None = None) -> Test:
    """
        Funkcja tworząca test 
    """
    if idPlikuCSV:
        raise NotImplementedError
    else:
        idPlikuCSV: str = "test.csv"
    if liczbaPytan:
        raise NotImplementedError
        
    with open(os.path.join(FOLDER_PYTAN, idPlikuCSV)) as plik: # Bład scieżki .\Backend\App.py
        lista_pytan: list[Pytanie] = []
        
        for P_ID, pytanie in enumerate(plik.readlines()):
            pytanie, *odpowiedi = pytanie.split("|")
            lista_pytan.append(Pytanie(P_ID=P_ID, TEKST=pytanie, ODPOWIDZI=odpowiedi, POPRAWNA=odpowiedi[0]))
    
    
    T_ID=randint(*ZAKRES_T_ID) #!!! DO POPRAWY/ Nie sprawdza czy test o danym id już istnieje
    test = Test(T_ID=T_ID, LISTA_PYTAN=lista_pytan)
    Lista_testow[T_ID] = test
    
    return test

@app.get("/all")
async def all():
    return Lista_testow

