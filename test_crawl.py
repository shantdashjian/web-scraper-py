import unittest
from crawl import normalize_url

class Test(unittest.TestCase):

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


if __name__ == "__main__":
    unittest.main()