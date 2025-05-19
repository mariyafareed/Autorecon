# Autorecon
AutoRecon is a Python-based automated reconnaissance tool for bug bounty hunters and penetration testers.

## Features

- Subdomain enumeration using Subfinder
- Port scanning using Nmap
- CLI interface with `--full` mode
- Modular and extendable

## Usage

```bash
git clone https://github.com/mariyfareed/autorecon.git
cd autorecon
python autorecon.py -d example.com --full
