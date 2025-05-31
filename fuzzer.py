import requests

def fuzz_directories(url):
    wordlist = ['admin', 'login', 'dashboard', 'upload', 'config']
    for word in wordlist:
        full_url = f"{url.rstrip('/')}/{word}"
        try:
            r = requests.get(full_url, timeout=5)
            if r.status_code == 200:
                print(f"[+] Found: {full_url}")
        except:
            pass
