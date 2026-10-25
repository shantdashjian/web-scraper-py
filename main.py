import asyncio
import sys

from async_crawler import crawl_site_async


async def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    BASE_URL = sys.argv[1]
    print(f"starting crawl of: {BASE_URL}")
    page_datas = await crawl_site_async(BASE_URL)
    for page_data in page_datas.values():
        print(f"Number of Pages Found: {len(page_data)}")
        for page_content in page_data.values():
            print(page_content)

if __name__ == "__main__":
    asyncio.run(main())
