from __future__ import annotations
from fastapi import FastAPI
import uvicorn

# Lokalne pliki
from datamodel import FastApiTags
from routes.router_teacher import ROUTER_NAUCZYCZIEL
from routes.router_student import ROUTER_UCZEN

# FastApi
# Opis tagów
TAGS_METADATA = [
    {
        "name": FastApiTags.NAUCZYCIEL,
        "description": "Tworzenie testów oraz ich kontrolowanie"
    },
    {
        "name": FastApiTags.UCZEN,
        "description": "Pobieranie arkuszy oraz wysyłanie odpowiedz"
    },
]

# Aplikacja
APP = FastAPI(title="TestCreator API",
              description="API służącze do przeprowadzania testów",
              version="0.0.3",
              openapi_tags=TAGS_METADATA)

APP.include_router(ROUTER_NAUCZYCZIEL, 
                   prefix=f"/{FastApiTags.NAUCZYCIEL.name.lower()}",
                   tags=[FastApiTags.NAUCZYCIEL])

APP.include_router(ROUTER_UCZEN, 
                   prefix=f"/{FastApiTags.UCZEN.name.lower()}",
                   tags=[FastApiTags.UCZEN])




if __name__ == "__main__":
    uvicorn.run(app="App:APP", host="0.0.0.0", port=8000, reload=False)
