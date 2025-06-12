from autorecon.commands import scan, webrecon, waf, fuzz
from autorecon.commands import subdomain, livedomain, webcrawl, findparams, findversions
import argparse
import socket
from autorecon.core.utils import parse_ports, get_top_ports, resolve_ip
import time
import sys
from colorama import init, Fore, Style
import platform
import subprocess
import ssl

def main():
    parser = argparse.ArgumentParser(prog="autorecon")
    subparsers = parser.add_subparsers(dest="command")

    # Existing modules
    webrecon.add_webrecon_subparser(subparsers)
    waf.add_waf_subparser(subparsers)
    fuzz.add_fuzz_subparser(subparsers)
    scan.add_scan_subparser(subparsers)

    # New modules
    subdomain.add_subdomain_subparser(subparsers)
    livedomain.add_livedomain_subparser(subparsers)
    webcrawl.add_webcrawl_subparser(subparsers)
    findparams.add_findparams_subparser(subparsers)
    findversions.add_findversions_subparser(subparsers)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
