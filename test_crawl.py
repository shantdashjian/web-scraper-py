import unittest
from crawl import extract_page_data, get_first_paragraph_from_html, get_heading_from_html, get_images_from_html, get_urls_from_html, normalize_url


class TestNormalize(unittest.TestCase):

    def test_https_no_end_slash(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_http_no_end_slash(self):
        input_url = "http://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_https_with_end_slash(self):
            input_url = "https://www.boot.dev/blog/path/"
            actual = normalize_url(input_url)
            expected = "www.boot.dev/blog/path"
            self.assertEqual(actual, expected)

    def test_http_with_end_slash(self):
            input_url = "http://www.boot.dev/blog/path/"
            actual = normalize_url(input_url)
            expected = "www.boot.dev/blog/path"
            self.assertEqual(actual, expected)


class TestExtractPageContent(unittest.TestCase):
     
    def test_get_heading_from_html_basic(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_h1_h2(self):
        input_body = "<html><body><h1>Test h1 Title</h1><h2>Test h2 Title</h2></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test h1 Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_h2(self):
        input_body = "<html><body><h2>Test h2 Title</h2></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test h2 Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_no_heading(self):
        input_body = "<html><body><p>Test Paragraph</p></body></html>"
        actual = get_heading_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_main_p(self):
        input_body = """<html><body>
            <p>p1</p>
            <p>p2</p>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "p1"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_p(self):
        input_body = """<html><body>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)


class ExtractLinksAndImages(unittest.TestCase):

    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/index.html"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/index.html"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_many(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/index.html"><span>Boot.dev index</span></a><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/index.html", "https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://example.com/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://example.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_missing_src(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ['ERROR: Missing img src']
        self.assertEqual(actual, expected)


class ExtractPageData(unittest.TestCase):

    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_p_in_main(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <main>
                <p>This is the first paragraph.</p>
            </main>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_no_img_src(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <main>
                <p>This is the first paragraph.</p>
            </main>
            <a href="/link1">Link 1</a>
            <img alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ['ERROR: Missing img src'],
        }
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()