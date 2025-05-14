from __future__ import annotations
from datamodel import Test, Pytanie, Uczen, T_ID_t, U_ID_t, P_ID_t
from httperror import HTTP_Not_Implemented, HTTP_Not_Test_find
from fastapi import FastAPI
import uvicorn
import os
import uuid


# Do zrobienia. Porawa funkji tworzenia testow oraz napisanie rzarzadania sciezka 
# Konfiguracja
NAZWA_GLOWNEGO_FOLDERU: str = "TestCreator"
NAZWA_FOLDERU_BACKEND: str = "Backend"
NAZWA_DOMYSLNEGO_TESTU: str = "test.csv"
FOLDER_PYTAN: str = "pliki_pytan" # Folder gdzie znajdują sie pliki z pytaniami

if os.getcwd().split("\\")[-1] == NAZWA_GLOWNEGO_FOLDERU:
    os.chdir(NAZWA_FOLDERU_BACKEND)

#Globalne zmiene
app = FastAPI()
Dzienik_Testow: dict[T_ID_t, Test] = {} 
    
# Do dokonczenia
@app.get("/nauczyciel/stworz_test")
def stworz_test(liczbaPytan: None = None, idPlikuCSV: None = None) -> Test:
    """
        Funkcja tworząca test 
    """
    if idPlikuCSV:
        raise HTTP_Not_Implemented
    else:
        idPlikuCSV: str = NAZWA_DOMYSLNEGO_TESTU
    if liczbaPytan:
        raise HTTP_Not_Implemented
    
    T_ID: T_ID_t = uuid.uuid4().hex
    lista_pytan: list[Pytanie] = []
    poprawne_odpowiedzi: dict[P_ID_t, str] = {}
    dzienik_uczniow: dict[U_ID_t, Uczen] = {}
        
    with open(os.path.join(FOLDER_PYTAN, idPlikuCSV)) as plik:         
        for P_ID, pytanie in enumerate(plik.readlines()):
            if pytanie.endswith("\n"):
                pytanie = pytanie[:-1]
            pytanie, *odpowiedi = pytanie.split("|")
            lista_pytan.append(Pytanie(P_ID=P_ID, TEKST=pytanie, ODPOWIDZI=odpowiedi))
            poprawne_odpowiedzi[P_ID] = odpowiedi[0]
    
    test = Test(T_ID=T_ID, LISTA_PYTAN=lista_pytan, DZIENIK_UCZNIOW=dzienik_uczniow, POPRAWNE_ODPOWIEDZI=poprawne_odpowiedzi)
    Dzienik_Testow[T_ID] = test
    return test

@app.get('/nauczyciel/zamkij_test/{T_ID}')
def zamknij_test(T_ID: T_ID_t) -> Test:
    raise HTTP_Not_Implemented

@app.get('/uczen/test/{T_ID}')
def wysylanie_testu(T_ID: T_ID_t) -> Test:
    test: Test = Dzienik_Testow.get(T_ID)
    if not test:
        raise HTTP_Not_Test_find
    
    test = test.model_copy()
    del test.POPRAWNE_ODPOWIEDZI
    
    return test

@app.get("/uczen/odpowiedzi/{T_ID}")
def pobieranie_odpowiedzi(T_ID: T_ID_t):
    raise HTTP_Not_Implemented

@app.get("/all")
async def all():
    return Dzienik_Testow

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

