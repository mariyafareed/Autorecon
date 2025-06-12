import argparse
import re

def detect_versions(file):
    with open(file, "r") as f:
        urls = [line.strip() for line in f]

    pattern = re.compile(r'v[\d\.]+|version[\d\.]+', re.IGNORECASE)
    print("[+] Detecting old versions:")
    for url in urls:
        if pattern.search(url):
            print(f"  [OLD VERSION] {url}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="File with URLs")
    args = parser.parse_args()
    detect_versions(args.file)
