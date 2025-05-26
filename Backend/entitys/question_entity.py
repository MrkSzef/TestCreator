
#  Pliki lokalne
from datamodel import ID_Pytanie_t, Odp_lista_t, Odp_t

class Pytanie:
    def __init__(self, ID: ID_Pytanie_t, tresc: str, odp: Odp_lista_t, odp_praw: Odp_t):
        self.ID: ID_Pytanie_t = ID
        
        self.tresc: str = tresc
        self.odp: Odp_lista_t = odp
        self.odp_praw: Odp_t = odp_praw  
