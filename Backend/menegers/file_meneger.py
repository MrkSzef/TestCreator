from __future__ import annotations
from fastapi import UploadFile
from typing import BinaryIO
import os

# Pliki lokalne
from httperror import HTTP_Not_Implemented
from entitys.file_entity import Plik

#TODO: Do poprawy 
class PlikMenadzer:
    SCIEZKA_ZAPISANE_PLIKI: str = os.path.join("saved_files")
    DOMYSLNE_KODOWANIE: str = "utf-8"
    def __init__(self, path: str = SCIEZKA_ZAPISANE_PLIKI):
        self.pliki: list[BinaryIO] = []

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        for plik in self.pliki:
            plik.close()
            
    def _add(self, plik: BinaryIO) -> None:
        self.pliki.append(plik)
            
    def list(self) -> list[str]:
        pliki: list[str] = os.listdir(self.SCIEZKA_ZAPISANE_PLIKI)
        return [plik for plik in pliki if plik.find(".csv") > 0]
    
    def otworz(self, plik_nazwa: str) -> Plik:
        try:
            plik = open(os.path.join(self.SCIEZKA_ZAPISANE_PLIKI, plik_nazwa), "rb")
        except FileNotFoundError:
            raise ValueError("Nie znaleziono pliku", f"nazwa: {plik_nazwa}")
            
        self._add(plik)
        
        return Plik(plik)                        
       
    def UploadFile(self, plik: UploadFile, zapisac: bool = False) -> Plik:
        self._add(plik.file)
        if plik.content_type != "text/csv":
            raise ValueError("Błedny typ pliku", "oczekiwano: text/csv", f"otrzymano: {plik.content_type}")
        
        if zapisac:
            self.zapis(plik.file, plik.filename)
        
        return Plik(plik.file, plik.filename)
    
    def zapis(self, plik: BinaryIO, plik_nazwa: str) -> None:
        try:
            with open(os.path.join(self.SCIEZKA_ZAPISANE_PLIKI, plik_nazwa), "+wb") as plik_lokalny:
                plik_lokalny.writelines(plik.readlines())
                plik.seek(0)
        except Exception as e:
            raise HTTP_Not_Implemented("Zgłosić, Bład zapisu", f"otrzymano: {type(plik)}", e.args)