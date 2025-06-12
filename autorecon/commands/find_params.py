import argparse

def find_parameters(file):
    with open(file, "r") as f:
        urls = [line.strip() for line in f]

    print("[+] Finding URLs with parameters:")
    for url in urls:
        if "?" in url and "=" in url:
            print(f"  [FOUND] {url}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="File with crawled URLs")
    args = parser.parse_args()
    find_parameters(args.file)
