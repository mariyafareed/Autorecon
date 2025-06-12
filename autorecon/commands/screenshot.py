from autorecon.core.screenshot import take_screenshot

def add_screenshot_subparser(subparsers):
    parser = subparsers.add_parser("screenshot", help="Take a screenshot of the web page")
    parser.add_argument("url", help="Target URL")
    parser.add_argument("--output", default="screenshot.png", help="Output screenshot file name")
    parser.set_defaults(func=handle_screenshot)

def handle_screenshot(args):
    take_screenshot(args.url, args.output)
