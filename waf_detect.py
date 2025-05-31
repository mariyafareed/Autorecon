import requests

def detect_waf(url):
    try:
        res = requests.get(url, timeout=10)
        waf_signatures = ['cloudflare', 'sucuri', 'akamai', 'f5', 'barracuda', 'imperva']
        server = res.headers.get('Server', '').lower()
        if any(sig in server for sig in waf_signatures):
            print(f"[+] WAF detected: {server}")
        else:
            print("[-] No known WAF detected.")
    except Exception as e:
        print("[-] Error during WAF detection:", e)
