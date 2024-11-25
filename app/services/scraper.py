# app/services/scraper.py

import requests
import re
from bs4 import BeautifulSoup

def scrape_emails_from_url(url: str):
    """
    Función que hace scraping de correos electrónicos desde una URL
    """
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"No se pudo acceder a la página: {url}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Buscar correos electrónicos usando expresión regular
    emails = set()
    for a_tag in soup.find_all("a", href=True):
        email_matches = re.findall(r"[\w\.-]+@[\w\.-]+", a_tag["href"])
        for email in email_matches:
            emails.add(email)
    
    return list(emails)
