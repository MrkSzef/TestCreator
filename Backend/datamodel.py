from __future__ import annotations
from typing import Annotated
from enum import Enum
from pydantic import BaseModel, Field

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
        2.4.0 - Informacja o użtkowniku
            2.4.1 - Imie
            2.4.2 - Nazwisko
        
    3.0.0 - Modele odpowiedzi
        3.1.0 - Pytanie
            3.1.1 - PytanieResponse
        3.2.0 - Arkusz
            3.2.1 - ArkuszResponse
        3.3.0 - Test
            3.3.1 - TestStworzonyResponse
            3.3.2 - TestWynikResponse
        3.1.0 - Urzutkownik
            3.1.1 - Uczen
"""

# 1.0.0 - Enumy
# 1.1.0 - FastApiTags
class FastApiTags(Enum):
    NAUCZYCIEL = "Nauczyciel"
    UCZEN = "Uczeń"

# 2.0.0 - Typy danych
# 2.1.0 - UUID
UUID_t = Annotated[str, Field(title="ID znakowo/numeryczne")]
UUID_Test_t = Annotated[UUID_t, Field(title="ID testu", description="ID testu")]
UUID_Urzytkownik_t = Annotated[UUID_t, Field(title="ID urzutkownika", description="ID urzutkownika")]

# 2.2.0 - ID
ID_t = Annotated[int, Field(title="ID numeryczne", ge=0)]
ID_Pytanie_t = Annotated[ID_t, Field(title="ID pytania", description="ID pytania")]
ID_Odp_t = Annotated[ID_t, Field(title="ID odpowiedzi", description="ID odpowiedzi")]

# 2.3.0 - Odp
Odp_t = Annotated[str, Field(title="Odpowiedź", description="Odpowiedź")]   
Odp_lista_t = Annotated[list[Odp_t], Field(title="Lista odpowiedzi")]
Odp_Klucz_t = Annotated[dict[ID_Pytanie_t, Odp_t], Field(title="Klucz odpowiedzi")]
Odp_Punkty_t = Annotated[int, Field(title="Punkty", ge=0)]

# 2.4.0 Informacje o uztkoniku
__podstawowa_skladnia = Annotated[str, Field(min_length=3,
                                                  max_length=51,
                                                  pattern="^[A-ZĘÓĄŚŁŻŹĆŃ][a-zęóąśłżźćń]*$")]
imie_t = Annotated[__podstawowa_skladnia, Field(title="Imie")]
nazwisko_t = Annotated[__podstawowa_skladnia, Field(title="Nazwisko")]

# 3.0.0 - Modele odpowiedzi
# 3.1.0 - Pytanie
# 3.1.1 - PytanieResponse 
class PytanieResponse(BaseModel):
    ID: ID_Pytanie_t
    tresc: str
    odp: Odp_lista_t

# 3.2.0 - Arkusz
# 3.2.1 - ArkuszResponse
class ArkuszResponse(BaseModel):
    pytania: list[PytanieResponse]

# 3.3.0 - Test
# 3.3.1 - TestStworzonyResponse
class TestStworzonyResponse(BaseModel):
    test_id: UUID_Test_t

# 3.3.2 - TestWynikResponse
class TestWynikResponse(BaseModel):
    punkty: Odp_Punkty_t
    pytania_bledne: list[ID_Pytanie_t]
    
# 3.3.3 - TestZamknietyResponse
class TestZamknietyResponse(BaseModel):
    wyniki: list[tuple[Uczen, TestWynikResponse]]

# 3.4.0 - Urztkownik
# 3.4.1 - Uczen
class Uczen(BaseModel):
    imie: imie_t
    nazwisko: nazwisko_t
