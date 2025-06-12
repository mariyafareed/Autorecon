# File: autorecon/core/osint.py

import shodan
import requests
from bs4 import BeautifulSoup
import time
import getpass

def shodan_lookup(target):
    api_key = getpass.getpass("Enter your Shodan API key: ")
    print(f"\n[+] Shodan OSINT Lookup for {target}")
    try:
        api = shodan.Shodan(api_key)
        result = api.search(target)
        print(f"[\u2713] Total Results: {result['total']}")
        for item in result['matches'][:5]:
            print(f"  IP: {item['ip_str']} | Port: {item['port']}")
            print(f"  Org: {item.get('org', 'N/A')}")
            print(f"  Data: {item['data'][:100]}...\n")
    except shodan.APIError as e:
        print(f"[\u2717] Shodan error: {e}")

def hunterio_lookup(domain):
    api_key = getpass.getpass("Enter your Hunter.io API key: ")
    print(f"\n[+] Hunter.io Email Discovery for {domain}")
    try:
        url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}"
        resp = requests.get(url).json()
        emails = resp.get("data", {}).get("emails", [])
        for email in emails[:5]:
            print(f"  Email: {email.get('value')}, Confidence: {email.get('confidence')}")
    except Exception as e:
        print(f"[\u2717] Hunter.io error: {e}")

def github_dorks(domain):
    print(f"\n[+] GitHub Dorking for sensitive info on {domain}")
    dorks = [
        f'"{domain}" password',
        f'"{domain}" API_KEY',
        f'"{domain}" AWS_SECRET_ACCESS_KEY',
        f'"{domain}" database'
    ]
    headers = {"User-Agent": "Mozilla/5.0"}
    for dork in dorks:
        print(f"\n[~] Searching: {dork}")
        try:
            q = requests.utils.quote(dork)
            url = f"https://github.com/search?q={q}"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                snippets = soup.find_all("div", {"class": "f4 text-normal"})
                print(f"  Found {len(snippets)} code snippets.")
            else:
                print(f"  GitHub returned status {response.status_code}")
            time.sleep(1)
        except Exception as e:
            print(f"  [\u2717] GitHub dorking error: {e}")

