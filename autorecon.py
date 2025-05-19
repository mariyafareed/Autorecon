import argparse
from modules import subdomain_enum, port_scan

def main():
    parser = argparse.ArgumentParser(description="AutoRecon - Automated Reconnaissance Tool")
    parser.add_argument("-d", "--domain", required=True, help="Target domain")
    parser.add_argument("--subdomains", action="store_true", help="Run subdomain enumeration")
    parser.add_argument("--ports", action="store_true", help="Run port scanning")
    parser.add_argument("--full", action="store_true", help="Run all recon modules")

    args = parser.parse_args()

    print(f"[+] Starting recon on: {args.domain}")

    if args.full or args.subdomains:
        subdomain_enum.run(args.domain)

    if args.full or args.ports:
        port_scan.run(args.domain)

    print("[+] Recon complete!")

if __name__ == "__main__":
    main()
