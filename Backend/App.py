from __future__ import annotations
from typing import Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Lokalne pliki
from datamodel import FastApiTags
from routes.router_teacher import ROUTER_NAUCZYCZIEL
from routes.router_student import ROUTER_UCZEN
from routes.router_files import ROUTER_PLIKI

# FastApi
# Opis tagów
TAGS_METADATA: list[dict[str, Any]] = [
    {
        "name": FastApiTags.NAUCZYCIEL,
        "description": "Tworzenie testów oraz ich kontrolowanie"
    },
    {
        "name": FastApiTags.UCZEN,
        "description": "Pobieranie arkuszy oraz wysyłanie odpowiedz"
    },
    {
        "name": FastApiTags.PLIKI,
        "description": "Zarządzanie plikami znajdującymi się na serwerze"
    }
]

origins: list[str] = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:5173",
]

# Aplikacja
APP = FastAPI(title="TestCreator API",
              description="API służącze do przeprowadzania testów",
              version="0.1.0",
              openapi_tags=TAGS_METADATA)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

APP.include_router(ROUTER_NAUCZYCZIEL, 
                   prefix=f"/{FastApiTags.NAUCZYCIEL.name.lower()}",
                   tags=[FastApiTags.NAUCZYCIEL])

APP.include_router(ROUTER_UCZEN, 
                   prefix=f"/{FastApiTags.UCZEN.name.lower()}",
                   tags=[FastApiTags.UCZEN])

APP.include_router(ROUTER_PLIKI,
                   prefix=f"/{FastApiTags.PLIKI.name.lower()}",
                   tags=[FastApiTags.PLIKI])


if __name__ == "__main__":
    uvicorn.run(app="App:APP", host="0.0.0.0", port=8000, reload=False)
