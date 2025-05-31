from .web_recon import web_recon
from .waf_detect import detect_waf
from .fuzzer import fuzz_directories
from .port_scan import scan_ports
from .visual_scan import take_screenshot

def main():
    target = input("Enter target URL (e.g., https://example.com): ")
    host = input("Enter host/IP for port scan (e.g., example.com or 1.2.3.4): ")

    print("\n[1] Web Recon")
    web_recon(target)

    print("\n[2] WAF Detection")
    detect_waf(target)

    print("\n[3] Fuzzing")
    fuzz_directories(target)

    print("\n[4] Port Scanning")
    scan_ports(host)

    print("\n[5] Visual Scan")
    take_screenshot(target)
