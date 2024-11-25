# app/main.py

from fastapi import FastAPI
from app.routes.scrape import router as scrape_router

# Crear una instancia de FastAPI
app = FastAPI()

# Incluir las rutas de scraping en la aplicación
app.include_router(scrape_router)
