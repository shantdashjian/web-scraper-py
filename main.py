import sys

from crawl import crawl_page, get_html


def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    BASE_URL = sys.argv[1]
    print(f"starting crawl of: {BASE_URL}")
    page_data = {}
    crawl_page(BASE_URL, BASE_URL, page_data)
    print(f"Number of Pages Found: {len(page_data)}")
    for _, page_content in page_data.items():
        print(page_content)

if __name__ == "__main__":
    main()
