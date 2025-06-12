from autorecon.core.dns_enum import dns_enum

def add_dnsenum_subparser(subparsers):
    parser = subparsers.add_parser("dnsenum", help="Enumerate DNS records")
    parser.add_argument("domain", help="Target domain")
    parser.set_defaults(func=handle_dns_enum)

def handle_dns_enum(args):
    dns_enum(args.domain)