import requests
import argparse

HEADERS = {"User-Agent": "Mozilla/5.0"}

def check_live(file):
    with open(file, "r") as f:
        domains = [line.strip() for line in f]
    
    print(f"[+] Checking live domains")
    for domain in domains:
        try:
            r = requests.get(f"http://{domain}", headers=HEADERS, timeout=3)
            if r.status_code < 400:
                print(f"  [LIVE] {domain}")
        except:
            continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="File with list of subdomains")
    args = parser.parse_args()
    check_live(args.file)
