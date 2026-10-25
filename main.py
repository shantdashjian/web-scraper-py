import asyncio
import sys

from async_crawler import crawl_site_async
from json_report import write_json_report


async def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)
    BASE_URL = sys.argv[1]
    print(f"starting crawl of: {BASE_URL}")
    max_concurrency = int(sys.argv[2])
    max_pages = int(sys.argv[3])
    page_datas = await crawl_site_async(BASE_URL, max_concurrency, max_pages)
    write_json_report(page_datas)

if __name__ == "__main__":
    asyncio.run(main())
