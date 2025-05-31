import socket

def scan_ports(host):
    common_ports = [21, 22, 23, 25, 53, 80, 110, 443, 8080]
    for port in common_ports:
        try:
            s = socket.create_connection((host, port), timeout=1)
            print(f"[+] Port {port} is open")
            s.close()
        except:
            pass
