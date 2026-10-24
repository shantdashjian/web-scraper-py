import unittest
from crawl import get_first_paragraph_from_html, get_heading_from_html, normalize_url


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


if __name__ == "__main__":
    unittest.main()