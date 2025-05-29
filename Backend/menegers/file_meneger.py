from __future__ import annotations
from typing import Any, BinaryIO, Self
import os

# Pliki lokalne
from datamodel import Plik_Nazwa_t
from entitys.file_entity import PlikEncDecCSV

#TODO: Do poprawy 
class PlikMenadzer:
    """ Wszystkie operacje polegającze na otwieraniu i tworzeniu plików powiny być opsługiwanie w
        contex-managerze
    """
    SCIEZKA_ZAPISANE_PLIKI: str = os.path.join("saved_files")
    DOMYSLNE_KODOWANIE: str = "utf-8"
    WIELKOSC_PORCII_ZAPISU: int = 1024 * 1024  # 1 MB
    def __init__(self, path: str = SCIEZKA_ZAPISANE_PLIKI) -> None:
        self.pliki: list[BinaryIO] = []

    def __enter__(self) -> Self:
        return self
    
    def __exit__(self, type, value, traceback) -> None:
        for plik in self.pliki:
            plik.close() if not plik.closed else None
        self.pliki.clear()
            
    def __str__(self) -> str:
        return f"PlikMenadzer(sciezka={self.SCIEZKA_ZAPISANE_PLIKI}, pliki={self.pliki})"
    
    def _add(self, plik: BinaryIO) -> None:
        self.pliki.append(plik)
            
    def lista(self) -> list[str]:
        pliki: list[str] = os.listdir(self.SCIEZKA_ZAPISANE_PLIKI)
        return [plik for plik in pliki if plik.find(".csv") > 0]
    
    def otworz(self, plik_nazwa: Plik_Nazwa_t) -> PlikEncDecCSV:
        try:
            plik = open(os.path.join(self.SCIEZKA_ZAPISANE_PLIKI, plik_nazwa), "rb")
        except FileNotFoundError:
            raise ValueError("Nie znaleziono pliku", f"nazwa: {plik_nazwa}")
            
        self._add(plik)
        
        return self.stworz(plik, plik_nazwa, zapisac=False)   
    
    def stworz(self, plik: BinaryIO, plik_nazwa: Plik_Nazwa_t | None, zapisac: bool) -> PlikEncDecCSV:
        if plik_nazwa is not None:
            if zapisac:
                plik = self.zapisz(plik, plik_nazwa, zamienic=True)
        else:
            plik_nazwa = "Plik_bez_nazwy"

        self._add(plik)
        plikEncDec: PlikEncDecCSV = PlikEncDecCSV(plik, plik_nazwa, self.DOMYSLNE_KODOWANIE)
        plikEncDec.decode()
        return plikEncDec
    
    def usun(self, plik_nazwa: str) -> None:
        sciezka_pliku: str = os.path.join(self.SCIEZKA_ZAPISANE_PLIKI, plik_nazwa)
        if not os.path.exists(sciezka_pliku):
            raise ValueError("Nie znaleziono pliku", f"nazwa: {plik_nazwa}")
        
        os.remove(sciezka_pliku)
    
    def zapisz(self, plik: BinaryIO, plik_nazwa: Plik_Nazwa_t, zamienic: bool = False) -> BinaryIO:
        plik_lokalny =  open(os.path.join(self.SCIEZKA_ZAPISANE_PLIKI, plik_nazwa), "+wb")
        
        while dane:= plik.read(self.WIELKOSC_PORCII_ZAPISU):
            plik_lokalny.write(dane)
            
        plik.seek(0)  # Resetowanie wskaźnika pliku na początek
        plik_lokalny.seek(0)  # Resetowanie wskaźnika pliku na początek
        
        if zamienic:
            plik.close() if not plik.closed else None
            return plik_lokalny
        
        plik_lokalny.close() if not plik_lokalny.closed else None
        return plik   

    def pobierz(self, plik_nazwa: Plik_Nazwa_t) -> dict[str, Any]: 
        sciezka_pliku: str = os.path.join(self.SCIEZKA_ZAPISANE_PLIKI, plik_nazwa)
        if not os.path.exists(sciezka_pliku):
            raise ValueError("Nie znaleziono pliku", f"nazwa: {plik_nazwa}")
        
        return {
                "path": sciezka_pliku,
                "media_type": "text/csv",
                "filename": plik_nazwa
               }