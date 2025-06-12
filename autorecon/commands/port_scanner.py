import socket
from concurrent.futures import ThreadPoolExecutor

def grab_banner(ip, port):
    try:
        with socket.create_connection((ip, port), timeout=2) as sock:
            sock.send(b'\r\n')
            return sock.recv(100).decode(errors='ignore').strip()
    except:
        return ''

def port_scan(target, ports, verbose=False, timing=3):
    ip = socket.gethostbyname(target)
    print(f"[+] Scanning {target} ({ip}) on ports: {ports}")

    thread_count = [1, 4, 8, 16, 32, 64][timing or 3]
    open_ports = []

    def scan_port(port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((ip, port))
                if result == 0:
                    banner = grab_banner(ip, port) if verbose else ''
                    print(f"[OPEN] Port {port} {f'- {banner}' if banner else ''}")
                    open_ports.append(port)
        except:
            pass

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        executor.map(scan_port, ports)

    print(f"\n[+] Scan complete. {len(open_ports)} open ports found.")
