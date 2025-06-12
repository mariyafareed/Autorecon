from autorecon.core.vuln_scanner import vuln_scan

def add_vulnscanner_subparser(subparsers):
    parser = subparsers.add_parser("vulnscanner", help="Scan for known CVEs using banner")
    parser.add_argument("banner", help="Service banner string")
    parser.set_defaults(func=handle_vulnscan)

def handle_vulnscan(args):
    vuln_scan(args.banner)