from __future__ import annotations
from typing import BinaryIO, Self
import os

# Pliki lokalne
from entitys.file_entity import PlikEncDecCSV

#TODO: Do poprawy 
class PlikMenadzer:
    SCIEZKA_ZAPISANE_PLIKI: str = os.path.join("saved_files")
    DOMYSLNE_KODOWANIE: str = "utf-8"
    def __init__(self, path: str = SCIEZKA_ZAPISANE_PLIKI) -> None:
        self.pliki: list[BinaryIO] = []

    def __enter__(self) -> Self:
        return self
    
    def __exit__(self, type, value, traceback) -> None:
        for plik in self.pliki:
            plik.close() if not plik.closed else None
        self.pliki.clear()
            
    def _add(self, plik: BinaryIO) -> None:
        self.pliki.append(plik)
            
    def list(self) -> list[str]:
        pliki: list[str] = os.listdir(self.SCIEZKA_ZAPISANE_PLIKI)
        return [plik for plik in pliki if plik.find(".csv") > 0]
    
    def otworz(self, plik_nazwa: str) -> PlikEncDecCSV:
        try:
            plik = open(os.path.join(self.SCIEZKA_ZAPISANE_PLIKI, plik_nazwa), "rb")
        except FileNotFoundError:
            raise ValueError("Nie znaleziono pliku", f"nazwa: {plik_nazwa}")
            
        self._add(plik)
        
        return self.stworz(plik, plik_nazwa, zapisac=False)   
    
    def stworz(self, plik: BinaryIO, plik_nazwa: str | None, zapisac: bool) -> PlikEncDecCSV:
        if plik_nazwa is not None:
            if zapisac:
                plik = self.zapisz(plik, plik_nazwa, zamienic=True)
        else:
            plik_nazwa = "Plik_bez_nazwy"

        self._add(plik)
        plikEncDec: PlikEncDecCSV = PlikEncDecCSV(plik, plik_nazwa, self.DOMYSLNE_KODOWANIE)
        plikEncDec.decode()
        return plikEncDec
    
    def zapisz(self, plik: BinaryIO, plik_nazwa: str, zamienic: bool = False) -> BinaryIO:
        plik_lokalny =  open(os.path.join(self.SCIEZKA_ZAPISANE_PLIKI, plik_nazwa), "+wb")
        plik_lokalny.writelines(plik.readlines())
        plik.seek(0)  # Resetowanie wskaźnika pliku na początek
        plik_lokalny.seek(0)  # Resetowanie wskaźnika pliku na początek
        
        if zamienic:
            plik.close() if not plik.closed else None
            return plik_lokalny
        
        return plik   
        
