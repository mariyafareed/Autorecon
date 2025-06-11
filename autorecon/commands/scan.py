from autorecon.core.ssl_analysis import analyze_tls
from autorecon.core.utils import parse_ports, get_top_ports, resolve_ip
import socket
import time
from colorama import init, Fore, Style
import ssl

init(autoreset=True)

def detect_os(target):
    try:
        print("\n[~] Attempting OS detection using TTL values...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((target, 80))
        ttl = sock.getsockopt(socket.IPPROTO_IP, socket.IP_TTL)
        sock.close()
        if ttl <= 64:
            print(f"{Fore.CYAN}[+] Likely OS: Linux/Unix (TTL={ttl})")
        elif ttl <= 128:
            print(f"{Fore.CYAN}[+] Likely OS: Windows (TTL={ttl})")
        else:
            print(f"{Fore.CYAN}[+] TTL={ttl}, OS unclear")
    except:
        print(f"{Fore.RED}[-] OS detection failed.")

def service_version_detection(target, port):
    try:
        with socket.create_connection((target, port), timeout=2) as sock:
            sock.sendall(b"HEAD / HTTP/1.1\r\nHost: example.com\r\n\r\n")
            response = sock.recv(1024)
            print(f"{Fore.MAGENTA}[SERVICE] Port {port} => {response.decode(errors='ignore').splitlines()[0]}")
    except:
        print(f"{Fore.YELLOW}[SERVICE] Port {port} => No response or unknown service")

def tech_stack_fingerprint(target, port):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((target, port), timeout=3) as sock:
            if port == 443:
                with context.wrap_socket(sock, server_hostname=target) as ssock:
                    cert = ssock.getpeercert()
                    print(f"{Fore.LIGHTBLUE_EX}[SSL] Certificate Issuer: {cert.get('issuer')}")
            else:
                sock.sendall(b"HEAD / HTTP/1.1\r\nHost: example.com\r\n\r\n")
                banner = sock.recv(1024).decode(errors='ignore')
                if "Server:" in banner:
                    for line in banner.splitlines():
                        if line.lower().startswith("server:"):
                            print(f"{Fore.LIGHTBLUE_EX}[TECH] Port {port} => {line.strip()}")
                            break
    except Exception as e:
        print(f"{Fore.YELLOW}[TECH] Port {port} => Tech detection failed ({e})")

def port_scan(target, ports, timeout=1, verbose=False, udp=False, output_file=None, fingerprint=False):
    open_ports = []
    proto = "UDP" if udp else "TCP"

    if len(ports) > 100:
        print(f"[+] Starting {proto} scan on {target} for {len(ports)} ports (range: {min(ports)}-{max(ports)})")
    else:
        ports_str = ', '.join(map(str, ports))
        print(f"[+] Starting {proto} scan on {target} for ports: {ports_str}")


    start_time = time.time()

    for port in ports:
        try:
            if udp:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(timeout)
                sock.sendto(b"\x00", (target, port))
                try:
                    data, _ = sock.recvfrom(1024)
                    print(f"{Fore.GREEN}[OPEN] UDP Port {port} => Response: {data.decode(errors='ignore').strip()}")
                    open_ports.append(port)
                except socket.timeout:
                    print(f"{Fore.YELLOW}[FILTERED] UDP Port {port}")
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                result = sock.connect_ex((target, port))
                if result == 0:
                    banner_info = ""
                    if verbose:
                        try:
                            sock.send(b"HEAD / HTTP/1.1\r\nHost: {}\r\n\r\n".format(target).encode())
                            banner = sock.recv(1024)
                            banner_info = f" => Banner: {banner.decode(errors='ignore').strip()}"
                        except:
                            banner_info = " => Banner: <error grabbing banner>"
                    print(f"{Fore.GREEN}[OPEN] Port {port}{banner_info}")
                    open_ports.append(port)
                    service_version_detection(target, port)
                    if fingerprint:
                        tech_stack_fingerprint(target, port)
            sock.close()
        except Exception:
            continue

    duration = round(time.time() - start_time, 2)
    result_summary = f"\n[+] Scan complete. {len(open_ports)} open {proto} ports found.\n⏰ Time Taken: {duration} seconds"
    print(result_summary)

    if output_file:
        with open(output_file, 'w') as f:
            f.write(f"Scan Results for {target}\n")
            for port in open_ports:
                f.write(f"[OPEN] {proto} Port {port}\n")
            f.write(result_summary + "\n")

    if not udp:
        detect_os(target)

    return open_ports

def run(args):
    if args.u:
        target = resolve_ip(args.u)

        if args.top_ports:
            ports = get_top_ports(args.top_ports)
        elif args.all_ports:
            ports = list(range(1, 65536))
        elif args.ports:
            ports = parse_ports(args.ports)
        else:
            ports = [80, 443]

        timeout_values = {
            0: 5, 1: 3, 2: 1.5, 3: 1, 4: 0.5, 5: 0.2
        }
        timeout = timeout_values.get(args.T, 1)

        port_scan(
            target,
            ports,
            timeout=timeout,
            verbose=args.verbose,
            udp=args.udp,
            output_file=args.output,
            fingerprint=args.fingerprint
        )

        if getattr(args, "ssl", False):
            analyze_tls(args.u, port=443)

def add_scan_subparser(subparsers):
    scan_parser = subparsers.add_parser("scan", help="Scan ports on a target")
    scan_parser.add_argument("-u", required=True, help="Target IP or domain")
    scan_parser.add_argument("-p", "--ports", help="Ports to scan (e.g. 80,443 or 1-100)")
    scan_parser.add_argument("--top-ports", type=int, help="Scan top N common ports")
    scan_parser.add_argument("--all-ports", action="store_true", help="Scan all 65535 ports")
    scan_parser.add_argument("-T", type=int, choices=range(0, 6), help="Timing template (0-5)")
    scan_parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output with banner grabbing")
    scan_parser.add_argument("--udp", action="store_true", help="Enable UDP port scanning")
    scan_parser.add_argument("--output", help="Save output to a file")
    scan_parser.add_argument("--fingerprint", action="store_true", help="Enable service fingerprinting")
    scan_parser.add_argument("--ssl", action="store_true", help="Perform SSL/TLS analysis on port 443")
    scan_parser.set_defaults(func=run)
