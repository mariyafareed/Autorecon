import requests
import argparse

HEADERS = {"User-Agent": "Mozilla/5.0 (ReconTool/1.0)"}

def enumerate_subdomains(domain):
    wordlist = ["www", "mail", "ftp", "dev", "test", "api", "blog"]
    print(f"[+] Subdomain enumeration for: {domain}")
    for sub in wordlist:
        url = f"http://{sub}.{domain}"
        try:
            res = requests.get(url, headers=HEADERS, timeout=2)
            if res.status_code < 400:
                print(f"  [LIVE] {sub}.{domain}")
        except:
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", required=True, help="Target domain")
    args = parser.parse_args()
    enumerate_subdomains(args.domain)
