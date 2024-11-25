# app/services/scraper.py

import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

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


# Función para obtener todos los enlaces en una página
def get_all_links(url):
    links = set()
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        # Encuentra todos los enlaces en la página
        for anchor in soup.find_all('a', href=True):
            link = anchor['href']
            full_link = urljoin(url, link)  # Convierte los enlaces relativos en absolutos
            # Filtra los enlaces internos
            if urlparse(full_link).netloc == urlparse(url).netloc:
                links.add(full_link)
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a la URL: {url}, Error: {e}")
    return links


# Función para hacer scraping de todas las páginas del sitio web
def crawl_website(start_url):
    visited = set()
    to_visit = {start_url}

    all_emails = set()

    while to_visit:
        url = to_visit.pop()
        if url not in visited:
            visited.add(url)
            print(f"Scraping {url}")

            # Extrae correos electrónicos de la página
            emails = scrape_emails(url)
            all_emails.update(emails)

            # Obtén todos los enlaces de la página
            links = get_all_links(url)

            # Añade los enlaces encontrados a la cola para visitar
            to_visit.update(links - visited)

    return all_emails


# Función para validar si un correo electrónico es válido
def is_valid_email(email):
    # Filtra correos con 'null' o con una cadena vacía
    if 'null' in email or not email:
        return False
    return True

# Función para extraer correos electrónicos de una página
def scrape_emails(url):
    emails = set()
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        # Usamos una expresión regular para encontrar correos electrónicos
        raw_emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', soup.text)

        # Filtra los correos electrónicos inválidos
        for email in raw_emails:
            if is_valid_email(email):
                emails.add(email)

    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a la URL: {url}, Error: {e}")
    
    return emails