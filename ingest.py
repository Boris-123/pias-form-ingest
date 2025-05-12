import os
import requests
from bs4 import BeautifulSoup

PAGE_URL = "https://singlife.com/en/form-library/"
CODY_API_KEY = os.getenv("CODY_API_KEY")

def fetch_pdf_links(url):
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    return {
        requests.compat.urljoin(url, a["href"])
        for a in soup.select('a[href$=".pdf"]')
    }

def ingest_to_cody(pdf_url):
    resp = requests.post(
        "https://api.cody.bot/v1/documents/webpage",
        headers={"Authorization": f"Bearer {CODY_API_KEY}"},
        json={"url": pdf_url}
    )
    resp.raise_for_status()
    print("Ingested:", pdf_url)

def main():
    for pdf in fetch_pdf_links(PAGE_URL):
        print("Processing", pdf)
        ingest_to_cody(pdf)

if __name__ == "__main__":
    main()
Add PDF ingest script
