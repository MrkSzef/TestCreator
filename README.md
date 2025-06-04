# Frontent i Backend do tworzenia testów online

## Wymagania
  
[![Static Badge](https://img.shields.io/badge/Python-3.12.6-green?style=for-the-badge&logo=python&labelColor=black&color=blue)](https://www.python.org/downloads/release/python-3126/)
[![Static Badge](https://img.shields.io/badge/FastApi-0.115.12-green?style=for-the-badge&logo=fastapi&labelColor=black&color=%23009485)](https://fastapi.tiangolo.com)
[![Static Badge](https://img.shields.io/badge/React-19.1-61DBFB?style=for-the-badge&logo=react&labelColor=black)](https://react.dev)
[![Static Badge](https://img.shields.io/badge/Node.js-22.15.0-darkgreen?style=for-the-badge&logo=node.js&labelColor=black)](https://nodejs.org/en)

## Opis

Podstawowa aplikacja webowa zawierającza narzędzia do tworzenia i przeprowadzania test online

### Nauczyciel

Nauczyciel tworzy test na stronie internetowej, przesyłając plik z pytaniami w formacie CSV oraz określając liczbę pytań, które mają znaleźć się w teście.
Po utworzeniu testu generowany jest unikalny kod, który nauczyciel przekazuje uczniom.
W trakcie trwania testu, nauczyciel na bieżąco widzi wyniki uczniów.
Po zakończeniu testu, nauczyciel klika przycisk zamykający test, co uniemożliwia dalsze udzielanie odpowiedzi.

### Uczeń 

Uczeń otrzymuje od nauczyciela unikalny kod testu, który umożliwia mu dostęp do losowo wygenerowanego arkusza z pytaniami.
Po udzieleniu odpowiedzi, uczeń otrzymuje informację o wyniku oraz numery pytań, w których popełnił błąd.

## Instalacja potrzebnych bibliotek

- Python - [pobierz](https://www.python.org/downloads/release/python-3126/)
- Node.js - [pobierz](https://nodejs.org/en/download)

Fast Api
```sh
pip install "fastapi[standard]"
```

React

Należy przejść do katalogu **`ReactApp`** a nastepnie wykonać polecenie
```sh
npm install
```
### Uruchamianie
Aby aplikacje ucuchomić należy wydać dwa polecennia

Pierwsze znajdującz się w folderze **`Backend`**

```sh
start python App.py
```

lub

```sh
start sciezka_do_interpretera_python\python.exe App.py
```

Drugie znajdując się w folderze **`ReactApp`**

```sh
start npm run dev
```

