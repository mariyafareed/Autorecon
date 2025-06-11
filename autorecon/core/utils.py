def parse_ports(ports_str):
    ports = set()
    for part in ports_str.split(','):
        if '-' in part:
            start, end = part.split('-')
            ports.update(range(int(start), int(end) + 1))
        else:
            ports.add(int(part))
    return sorted(ports)

def get_top_ports(n):
    # Normally this would be loaded from a file or list sorted by frequency
    top_ports = [80, 443, 21, 22, 23, 25, 53, 110, 139, 445, 8080, 3306, 1433, 53, 8443]  # sample
    return top_ports[:n]