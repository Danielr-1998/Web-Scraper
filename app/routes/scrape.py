# app/routes/scrape.py

from fastapi import APIRouter, HTTPException
from app.services.scraper import scrape_emails_from_url

router = APIRouter()

@router.get("/scrape/")
async def get_emails(url: str):
    """
    Ruta para hacer scraping de correos electrónicos desde una URL
    """
    try:
        emails = scrape_emails_from_url(url)
        if not emails:
            raise HTTPException(status_code=404, detail="No se encontraron correos electrónicos.")
        return {"emails": emails}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
