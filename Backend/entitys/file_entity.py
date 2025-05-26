from typing import BinaryIO, Generator

class Plik:
    def __init__(self, plik: BinaryIO, plik_nazwa: str):
        self.plik:  BinaryIO = plik
        self.plik_nazwa = plik_nazwa
    #TODO: Do poprawy
    def decode(self, sep: str = "|") -> Generator[list[str], None, None]:
        while wiersz := self.plik.readline():
            wiersz_str: str = str(wiersz, encoding="utf_8").strip("\n\r")
            yield wiersz_str.split("|")

    def encode(self):
        raise NotImplementedError()