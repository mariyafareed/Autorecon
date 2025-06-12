import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import warnings
warnings.filterwarnings("ignore")
from autorecon.core.web_recon import web_recon

def web_recon(target_url):
    print(f"\n[+] Starting Web Recon on {target_url}")
    try:
        response = requests.get(target_url, timeout=10, verify=False)
        print(f"[+] Status Code: {response.status_code}")

        headers = response.headers
        print("[+] Headers:")
        for key, value in headers.items():
            print(f"    {key}: {value}")

        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else "N/A"
        print(f"[+] Page Title: {title}")

        print("[+] Extracting assets (JS, CSS, images)...")
        tags = {"script": "src", "link": "href", "img": "src"}
        for tag, attr in tags.items():
            for element in soup.find_all(tag):
                url = element.get(attr)
                if url:
                    full_url = urljoin(target_url, url)
                    print(f"    {tag.upper()}: {full_url}")

        print("[+] Checking for common files...")
        for path in ["robots.txt", "sitemap.xml", ".env"]:
            full = urljoin(target_url, path)
            r = requests.get(full, timeout=5, verify=False)
            if r.status_code == 200:
                print(f"    Found: {full}")

        print("[+] Detecting login/admin paths...")
        for path in ["admin", "login", "dashboard", "cpanel"]:
            full = urljoin(target_url, path)
            r = requests.get(full, timeout=5, verify=False)
            if r.status_code in [200, 401, 403]:
                print(f"    Possible Panel: {full} [{r.status_code}]")

        print("[+] Detecting technologies from headers...")
        tech_stack = []
        server = headers.get("Server", "")
        powered_by = headers.get("X-Powered-By", "")
        content_type = headers.get("Content-Type", "")

        if "apache" in server.lower():
            tech_stack.append("Apache")
        if "nginx" in server.lower():
            tech_stack.append("Nginx")
        if "php" in powered_by.lower():
            tech_stack.append("PHP")
        if "asp" in powered_by.lower():
            tech_stack.append("ASP.NET")
        if "application/json" in content_type:
            tech_stack.append("JSON API")

        if tech_stack:
            print(f"    Identified Technologies: {', '.join(tech_stack)}")
        else:
            print("    No identifiable technologies via headers.")

    except requests.RequestException as e:
        print(f"[-] Error during web recon: {e}")


    def add_webrecon_subparser(subparsers):
        parser = subparsers.add_parser("webrecon", help="Perform web recon / footprinting")
        parser.add_argument("url", help="Target URL")
        parser.set_defaults(func=handle_webrecon)

    def handle_webrecon(args):
        web_recon(args.url)
    