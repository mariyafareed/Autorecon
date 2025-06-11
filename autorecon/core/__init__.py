def parse_ports(port_str):
    ports = []
    for part in port_str.split(','):
        if '-' in part:
            start, end = part.split('-')
            ports.extend(range(int(start), int(end)+1))
        else:
            ports.append(int(part))
    return ports

def get_top_ports(n):
    common_ports = [80, 443, 21, 22, 23, 25, 53, 110, 139, 143, 445, 3306, 3389, 8080]
    return common_ports[:n]
