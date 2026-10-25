from urllib.parse import urljoin, urlsplit
from bs4 import BeautifulSoup


def normalize_url(url):
    url_parts = urlsplit(url)
    netloc = url_parts.netloc
    path = url_parts.path
    if path[-1] == "/":
        path = path[:-1]
    return f"{netloc}{path}"


def get_heading_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    h1s = soup.find_all("h1", limit=1)
    if len(h1s) > 0:
        return h1s[0].get_text()
    h2s = soup.find_all("h2", limit=1)
    if len(h2s) > 0:
        return h2s[0].get_text()
    return ""


def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    mains = soup.find_all("main", limit=1)
    if len(mains) > 0:
        ps = mains[0].find_all("p", limit=1)
        if len(ps) > 0:
            return ps[0].get_text()
    ps = soup.find_all("p", limit=1)
    if len(ps) > 0:
        return ps[0].get_text()
    return ""


def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    anchors = soup.find_all("a")
    urls = []
    for anchor in anchors:
        urls.append(urljoin(base_url, anchor.get("href")))
    return urls


def get_images_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    imgs = soup.find_all("img")
    urls = []
    for img in imgs:
        urls.append(urljoin(base_url, img.get("src", "ERROR: Missing img src")))
    return urls
