import requests
from autorecon.core.waf_identification import identify_waf

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

    def add_waf_subparser(subparsers):
        parser = subparsers.add_parser("waf", help="Detect WAF on target")
        parser.add_argument("url", help="Target URL")
        parser.set_defaults(func=handle_waf)

    def handle_waf(args):
        identify_waf(args.url)