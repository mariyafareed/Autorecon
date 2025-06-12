import requests
from bs4 import BeautifulSoup
import argparse
from urllib.parse import urlparse

HEADERS = {"User-Agent": "Mozilla/5.0"}

def web_crawl(url, depth=2):
    visited = set()
    to_visit = [url]

    for _ in range(depth):
        next_links = []
        for link in to_visit:
            if link in visited:
                continue
            visited.add(link)
            try:
                r = requests.get(link, headers=HEADERS, timeout=3)
                soup = BeautifulSoup(r.text, 'html.parser')
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    if href.startswith("http"):
                        next_links.append(href)
                    elif href.startswith("/"):
                        parsed = urlparse(url)
                        full = f"{parsed.scheme}://{parsed.netloc}{href}"
                        next_links.append(full)
            except:
                continue
        to_visit = next_links

    for link in visited:
        print(f"  [CRAWLED] {link}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="Target base URL")
    args = parser.parse_args()
    web_crawl(args.url)
