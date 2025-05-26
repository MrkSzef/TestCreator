from __future__ import annotations
from typing import Annotated
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field

"""
    1.0.0 - Enumy
        1.1.0 - FastApiTags
    
    2.0.0 - typów danych
        2.1.0 - UUID
        2.2.0 - ID
        2.3.0 - Odp
            2.3.1 - Odp_t
                        Pojedyncza odpowiedz
            2.3.2 - Odp_Lista_t
                        Wiele odpowiedzi lista
            2.3.3 - Odp_Klucz_t
                        Odpowiedzi dla danego pytania
            2.3.4 - Odp_Punkty_t
            2.3.5 - Odp_Wyniki_t
            2.3.6 - Odp_Uczen_t
        2.4.0 - Pytania
        2.5.0 - Informacja o użtkowniku
            2.4.1 - Imie_t
            2.4.2 - Nazwisko_t
        2.5.0 - Test
            2.5.1 - Test_Status_t           
        
    3.0.0 - Modele odpowiedzi
        3.1.0 - Pytanie
            3.1.1 - PytanieResponse
        3.2.0 - Arkusz
            3.2.1 - ArkuszResponse
        3.3.0 - Test
            3.3.1 - TestStworzonyResponse
            3.3.2 - TestWynikResponse
            3.3.3 - 
            3.3.4 - TestInfoResponse
        3.1.0 - Urzutkownik
            3.4.1 - UczenResponse
            3.4.2 - UczenWynikResponse
"""

# 1.0.0 - Enumy
# 1.1.0 - FastApiTags
class FastApiTags(Enum):
    NAUCZYCIEL = "Nauczyciel"
    UCZEN = "Uczeń"
    PLIKI = "Pliki"
    
# 2.0.0 - Typy danych
# 2.1.0 - UUID
UUID_t = Annotated[str, Field(title="ID znakowo/numeryczne", examples=["db1a21b08bee4e5c888f413178e29a53", "30318450a4ac4b67b4c57e3a5cd83c1f"])]
UUID_Test_t = Annotated[UUID_t, Field(title="ID testu", description="ID testu")]
UUID_Uzytkownik_t = Annotated[UUID_t, Field(title="ID uzutkownika", description="ID uzutkownika")]

# 2.2.0 - ID
ID_t = Annotated[int, Field(title="ID numeryczne", ge=0, examples=[10, 2, 31, 19])]
ID_Pytanie_t = Annotated[ID_t, Field(title="ID pytania", description="ID pytania")]
ID_Odp_t = Annotated[ID_t, Field(title="ID odpowiedzi", description="ID odpowiedzi")]

# 2.3.0 - Odp
Odp_t = Annotated[str, Field(title="Odpowiedź", description="Odpowiedź", examples=["Odp a", "Odp b"])]   
Odp_lista_t = Annotated[list[Odp_t], Field(title="Lista odpowiedzi", examples=[["Odp a", "Odp b"], ["Odp c", "Odp d"]])]
Odp_Klucz_t = Annotated[dict[ID_Pytanie_t, Odp_t], Field(title="Klucz odpowiedzi", description="Przyporządkowuje id pytania do odpowiedzi", examples=[{4: "Odp a", 5: "Odp c"}])]
Odp_Punkty_t = Annotated[int, Field(title="Punkty", description="Liczba punktów", ge=0, examples=[1, 20, 5, 0])]

# 2.4.0 - Pytania
Pytania_lista_t = Annotated[list[ID_Pytanie_t], Field(title="Lista pytan")]

# 2.5.0 Informacje o uztkoniku
__podstawowa_skladnia = Annotated[str, Field(min_length=3,
                                                  max_length=51,
                                                  pattern="^[A-ZĘÓĄŚŁŻŹĆŃ][a-zęóąśłżźćń]*$")]
imie_t = Annotated[__podstawowa_skladnia, Field(title="Imie", description="Imie osoby", examples=["Stefan", "Marta"])]
nazwisko_t = Annotated[__podstawowa_skladnia, Field(title="Nazwisko", description="Nazwiskow osoby", examples=["Stanowski", "Nieśmiałek"])]

# 2.5.0 Test
# 2.5.1 TestStatus_t
Test_Status_t = Annotated[bool, Field(title="Status testu", description="Wartoś określającza czy test jest otwary czy zamkniety.\
\n\tOtwary - Można udzielać odpowiedz\
\n\tZamkniety - Test już się zakończył i niemożna udzielać odpowiedzi",
examples=[f"{False} - Test otwarty", f"{True} - Test zamknięty"])]

# 3.0.0 - Modele odpowiedzi
CONFIG_DICT = ConfigDict(frozen=True)
# 3.1.0 - Pytanie
# 3.1.1 - PytanieResponse 
class PytanieResponse(BaseModel):
    model_config = CONFIG_DICT
    ID: ID_Pytanie_t
    tresc: str
    odp: Odp_lista_t

# 3.2.0 - Arkusz
# 3.2.1 - ArkuszResponse
class ArkuszResponse(BaseModel):
    model_config = CONFIG_DICT
    pytania: list[PytanieResponse]

# 3.3.0 - Test
# 3.3.1 - TestStworzonyResponse
class TestStworzonyResponse(BaseModel):
    model_config = CONFIG_DICT
    test_id: UUID_Test_t

# 3.3.2 - TestWynikResponse
class TestWynikResponse(BaseModel):
    model_config = CONFIG_DICT
    punkty: Odp_Punkty_t
    pytania_bledne: Pytania_lista_t
  
# 3.3.4 - TestInfoResponse
class TestInfoResponse(BaseModel):
    model_config = CONFIG_DICT
    ID: UUID_Test_t
    
    zamkniety: Test_Status_t
    
    pytania:  list[PytanieResponse]
    pytania_na_arkusz: int
    klucz_odp: Odp_Klucz_t
    
    uczestnicy_odpowiedzi: list[UczenWynikResponse]

# 3.4.0 - Urztkownik
# 3.4.1 - UczenResponse
class UczenResponse(BaseModel):
    model_config = CONFIG_DICT
    
    imie: imie_t
    nazwisko: nazwisko_t

# 3.4.2 - UczenWynikResponse
class UczenWynikResponse(BaseModel):
    model_config = CONFIG_DICT
    
    klucz_odp: Odp_Klucz_t
    uczen: UczenResponse
    wynik: TestWynikResponse    
