from autorecon.commands import scan
import argparse
import socket
import argparse
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

    # Attach the scan subcommand
    scan.add_scan_subparser(subparsers)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
