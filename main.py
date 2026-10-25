import sys

from crawl import get_html


def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    BASE_URL = sys.argv[1]
    print(f"starting crawl of: {BASE_URL}")
    html = get_html(BASE_URL)
    print(html)
    

if __name__ == "__main__":
    main()
