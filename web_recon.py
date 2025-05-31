import requests
from bs4 import BeautifulSoup

def web_recon(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        print("[+] Title:", soup.title.string if soup.title else "No title found")
        print("[+] Headers:")
        for k, v in res.headers.items():
            print(f"  {k}: {v}")
    except Exception as e:
        print("[-] Error during web recon:", e)
