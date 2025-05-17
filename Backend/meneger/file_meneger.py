from __future__ import annotations
from fastapi import UploadFile
from typing import Generator

# Do poprawy 
class PlikMenadzer:
    def __init__(self, plik: UploadFile):
        self.plik: UploadFile = plik

        if plik.content_type != "text/csv":
            raise ValueError()

    def decode(self, sep: str = "|") -> Generator[list[str]]:
        wiersz: bytes
        while wiersz := self.plik.file.readline():
            wiersz_str: str = str(wiersz, encoding="utf_8").strip("\n\r")
            yield wiersz_str.split("|")

    def encode(self):
        raise NotImplementedError()
