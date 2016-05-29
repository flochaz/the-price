import unittest
from urllib2 import HTTPError
from amazon.api import SearchException

import mock

from the_price.search_engines.amazon_price_finder import  AmazonPriceFinder
import the_price


class TestAmazonPriceFinder(unittest.TestCase):

    @mock.patch('the_price.search_engines.amazon_price_finder.ENCRYPTED_AMAZON_ACCESS_KEY', 'CiBcAIDW86v+VtwF1daIZ/rGEHGVM5uMbYXqq8HaWbtoZhKXAQEBAgB4XACA1vOr/lbcBdXWiGf6xhBxlTObjG2F6qvB2lm7aGYAAABuMGwGCSqGSIb3DQEHBqBfMF0CAQAwWAYJKoZIhvcNAQcBMB4GCWCGSAFlAwQBLjARBAwUuYBc9YjGGlPjGZQCARCAK1BnG02jRgCbcUdxEB902q5pFMiOvEFMwOyNKeieCZ1TEhy5H8yzfRFpm2g=')
    def test_search_with_wrong_creds(self):
        finder = AmazonPriceFinder()
        try:
            finder.find('kindle')
            self.fail()
        except Exception as ex:
            # expect a InvalidCiphertextException
            self.assertIsInstance(ex, Exception)

    def test_search_with_right_creds_and_multi_word_item(self):
        finder = AmazonPriceFinder()
        original_description, price, currency = finder.find('kindle fire')
        self.assertIsNotNone(original_description)
        self.assertIsNotNone(price)
        self.assertIsNotNone(currency)

    def test_search_with_right_creds_and_single_word_item(self):
        finder = AmazonPriceFinder()
        original_description, price, currency = finder.find('kindle')
        self.assertIsNotNone(original_description)
        self.assertIsNotNone(price)
        self.assertIsNotNone(currency)

    def test_search_no_existing_item(self):
        try:
            finder = AmazonPriceFinder()
            finder.find('bdgjudmymhrdm')
            self.fail()
        except Exception as ex:
            self.assertIsInstance(ex, SearchException)

