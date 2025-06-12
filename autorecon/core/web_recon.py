import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import warnings
warnings.filterwarnings("ignore")

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

    except requests.RequestException as e:
        print(f"[-] Error during web recon: {e}")


# -------- core/waf_identification.py --------
def identify_waf(target_url):
    print(f"\n[+] Starting WAF Detection on {target_url}")
    try:
        headers = requests.get(target_url, timeout=10, verify=False).headers
        waf_indicators = [
            "X-Sucuri-ID", "X-CDN", "X-Cache", "Server", "CF-RAY", "X-Akamai",
            "X-Powered-By", "X-FireEye", "X-Imperva", "X-WAF", "X-Distil-CS"
        ]
        for header in waf_indicators:
            if header in headers:
                print(f"    Detected WAF-related header: {header} -> {headers[header]}")

        print("[+] Sending WAF test payload...")
        test_url = f"{target_url}?q=<script>alert('x')</script>"
        r = requests.get(test_url, timeout=10, verify=False)
        if r.status_code in [403, 406, 501] or "waf" in r.text.lower():
            print("    WAF likely present based on response to malicious input")

    except requests.RequestException as e:
        print(f"[-] Error during WAF detection: {e}")

