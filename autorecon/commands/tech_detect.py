from autorecon.core.tech_detect import detect_technologies

def add_techdetect_subparser(subparsers):
    parser = subparsers.add_parser("techdetect", help="Detect technologies from page/scripts")
    parser.add_argument("url", help="Target URL")
    parser.set_defaults(func=handle_techdetect)

def handle_techdetect(args):
    detect_technologies(args.url)
