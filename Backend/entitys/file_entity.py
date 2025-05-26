from __future__ import annotations

from typing import BinaryIO, Generator

# Klasa do obsługi plików CSV
class PlikEncDecCSV():
    def __init__(self, plik: BinaryIO, plik_nazwa: str, kodowanie) -> None:
        self.plik:  BinaryIO = plik
        self.plik_nazwa = plik_nazwa
        self.kodowanie: str = kodowanie
        self.plik.seek(0)  # Resetowanie wskaźnika pliku na początek
        
    def decode(self, sep: str = "|") -> Generator[list[str], None, None]:
        while wiersz := self.plik.readline():
            wiersz_str: str = str(wiersz, encoding=self.kodowanie).strip("\n\r")
            yield wiersz_str.split(sep)

    def encode(self, nazwa: str, wartosci: list[str], sep: str = "|") -> None:
        self.plik.write(f"{nazwa}{sep}{sep.join(wartosci)}\n".encode(self.kodowanie))
