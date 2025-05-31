import argparse
from urllib.parse import urlparse

# import your functions here (or define them above)
# web_footprinting(), detect_waf(), etc.

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AutoRecon - Custom Web Recon Tool")
    parser.add_argument("url", help="Target URL (e.g. http://example.com)")
    parser.add_argument("--footprint", action="store_true", help="Run web footprinting")
    parser.add_argument("--waf", action="store_true", help="Detect WAF")
    parser.add_argument("--fuzz", action="store_true", help="Run directory fuzzing")
    parser.add_argument("--scan", action="store_true", help="Run port scan")
    parser.add_argument("--screenshot", action="store_true", help="Take screenshot")
    args = parser.parse_args()

    target = args.url
    hostname = urlparse(target).hostname

    if args.footprint:
        web_footprinting(target)
    if args.waf:
        detect_waf(target)
    if args.fuzz:
        wordlist = ["admin", "login", "dashboard", "uploads"]
        directory_fuzz(target, wordlist)
    if args.scan:
        port_scan(hostname)
    if args.screenshot:
        take_screenshot(target)
