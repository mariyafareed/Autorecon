import socket
import ssl
import hashlib
import datetime
from colorama import Fore, Style
import http.client

def get_cert_fingerprint(cert_der):
    sha256 = hashlib.sha256(cert_der).hexdigest()
    return ':'.join(sha256[i:i+2] for i in range(0, len(sha256), 2)).upper()

def get_expiry_status(expiry_str):
    expiry = datetime.datetime.strptime(expiry_str, '%b %d %H:%M:%S %Y %Z')
    now = datetime.datetime.utcnow()
    days_left = (expiry - now).days

    if days_left < 0:
        return f"{Fore.RED}[EXPIRED]{Style.RESET_ALL}", days_left
    elif days_left < 30:
        return f"{Fore.YELLOW}[EXPIRING SOON]{Style.RESET_ALL}", days_left
    else:
        return f"{Fore.GREEN}[VALID]{Style.RESET_ALL}", days_left

def check_hsts(hostname):
    try:
        conn = http.client.HTTPSConnection(hostname, timeout=5)
        conn.request("GET", "/")
        res = conn.getresponse()
        hsts = res.getheader("Strict-Transport-Security")
        if hsts:
            print(f"{Fore.GREEN}[+] HSTS Detected: {hsts}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[-] HSTS Not Detected{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] HSTS check failed: {e}{Style.RESET_ALL}")

def analyze_tls(hostname, port=443, timeout=5, show_hsts=True):
    print(f"\n{Fore.CYAN}[+] Starting SSL/TLS analysis for {hostname}:{port}{Style.RESET_ALL}")

    context = ssl.create_default_context()

    try:
        with socket.create_connection((hostname, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                cert_der = ssock.getpeercert(True)
                cipher = ssock.cipher()
                tls_version = ssock.version()

                # Output TLS version and cipher
                print(f"{Fore.GREEN}[*] TLS Version: {tls_version}")
                print(f"[*] Cipher: {cipher[0]} ({cipher[1]} bits, {cipher[2]}){Style.RESET_ALL}")

                # Certificate Information
                print(f"{Fore.BLUE}[+] Certificate Information:{Style.RESET_ALL}")
                print(f"    Subject: {cert.get('subject')}")
                print(f"    Issuer: {cert.get('issuer')}")
                print(f"    Not Before: {cert.get('notBefore')}")
                print(f"    Not After: {cert.get('notAfter')}")

                # Expiry check
                status, days = get_expiry_status(cert.get('notAfter'))
                print(f"    Expiry Status: {status} (in {days} days)")

                # Fingerprint
                fingerprint = get_cert_fingerprint(cert_der)
                print(f"    SHA256 Fingerprint: {fingerprint}")

                # HSTS check
                if show_hsts:
                    check_hsts(hostname)

    except ssl.SSLError as e:
        print(f"{Fore.RED}[!] SSL error: {e}{Style.RESET_ALL}")
    except socket.timeout:
        print(f"{Fore.RED}[!] Connection to {hostname}:{port} timed out{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Unexpected error: {e}{Style.RESET_ALL}")
