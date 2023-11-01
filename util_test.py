import unittest
from util import is_valid_url, explore, extract_base_url

class TestClass(unittest.TestCase):

    def test_is_valid_url(self):
        is_valid = is_valid_url("http://valid-url.com")
        self.assertEqual(True, is_valid)

    def test_is_valid_url_None(self):
        is_valid = is_valid_url(None)
        self.assertEqual(False, is_valid)

    def test_explore(self):
        content = '<html><body><a href="http://www.google.com"></body></html>'
        value = explore(bytes(content, 'utf-8'))
        self.assertEqual(["http://www.google.com"], value)

    def test_extract_base_url(self):
        url = 'http://test.ua.com/fb/1234/today'
        extracted_url = extract_base_url(url)

        self.assertEqual("http://test.ua.com", extracted_url)
    
    def test_extract_base_url(self):
        url = 'httpx://test...,ua.com/fb/1234/today'
        extracted_url = extract_base_url(url)

        self.assertEqual("http://test.ua.com", extracted_url)




if __name__ == '__main__':
  unittest.main()