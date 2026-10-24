from urllib.parse import urlsplit


def normalize_url(url):
    url_parts = urlsplit(url)
    netloc = url_parts.netloc
    path = url_parts.path
    if path[-1] == "/":
        path = path[:-1]
    return f"{netloc}{path}"