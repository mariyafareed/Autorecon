from autorecon.core.osint import osint_lookup

def add_osint_subparser(subparsers):
    parser = subparsers.add_parser("osint", help="Gather WHOIS and OSINT info")
    parser.add_argument("domain", help="Target domain")
    parser.set_defaults(func=handle_osint)

def handle_osint(args):
    osint_lookup(args.domain)
