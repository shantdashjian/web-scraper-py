import asyncio

import aiohttp
from requests.compat import urlsplit

from crawl import extract_page_data, normalize_url


class AsyncCrawler:
    def __init__(self, base_url, max_concurrency, max_pages):
        self.base_url = base_url
        self.base_domain = urlsplit(base_url).netloc
        self.page_data = {}
        self.visited = set()
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks = set()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ):
        if self.session is not None:
            await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if self.should_stop:
                return False
            if normalized_url in self.visited:
                return False
            if len(self.visited) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                return False
            self.visited.add(normalized_url)
            return True

    async def get_html(self, url):
        if self.session is None:
            return None
        try:
            async with self.session.get(
                url, headers={"User-Agent": "BootCrawler/1.0"}
            ) as response:
                if response.status >= 400:
                    print(f"Error: HTTP {response.status} for {url}")
                    return None

                content_type = response.headers.get("content-type", "")
                if "text/html" not in content_type:
                    print(f"Error: Non-HTML content {content_type} for {url}")
                    return None

                return await response.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    async def crawl_page(self, current_url):
        if self.should_stop:
            return
        
        current_url_obj = urlsplit(current_url)
        if current_url_obj.netloc != self.base_domain:
            return

        normalized_url = normalize_url(current_url)

        is_new = await self.add_page_visit(normalized_url)
        if not is_new:
            return

        async with self.semaphore:
            print(
                f"Crawling {current_url} (Active: {self.max_concurrency - self.semaphore._value})"
            )
            html = await self.get_html(current_url)
            if html is None:
                return

            page_info = extract_page_data(html, current_url)
            async with self.lock:
                self.page_data[normalized_url] = page_info

            next_urls = page_info["outgoing_links"]

        if self.should_stop:
            return

        tasks = []
        for next_url in next_urls:
            task = asyncio.create_task(self.crawl_page(next_url))
            tasks.append(task)
            self.all_tasks.add(task)

        if tasks:
            try:
                await asyncio.gather(*tasks, return_exceptions=True)
            finally:
                for task in tasks:
                    self.all_tasks.discard(task)

    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data


async def crawl_site_async(base_url, max_concurrency, max_pages):
    async with AsyncCrawler(base_url, max_concurrency, max_pages) as crawler:
        return await crawler.crawl()
