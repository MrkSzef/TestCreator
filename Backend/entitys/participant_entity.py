
from datamodel import Pytania_lista_t, imie_t, nazwisko_t, Odp_Klucz_t, Odp_Punkty_t

class Uczestnik:
    def __init__(self, imie: imie_t, nazwisko: nazwisko_t, odpowiedzi: Odp_Klucz_t):
        self.imie: imie_t = imie
        self.nazwisko: nazwisko_t = nazwisko
        
        self.odpowiedzi: Odp_Klucz_t = odpowiedzi
        self.punkty: Odp_Punkty_t = 0
        self.pytania_blende: Pytania_lista_t = []