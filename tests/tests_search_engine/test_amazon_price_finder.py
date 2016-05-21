import unittest
from urllib2 import HTTPError

import mock

from the_price.search_engine.amazon_price_finder import  AmazonPriceFinder
import the_price


class TestAmazonPriceFinder(unittest.TestCase):

    @mock.patch('the_price.search_engine.amazon_price_finder.ENCRYPTED_AMAZON_ACCESS_KEY', 'CiBcAIDW86v+VtwF1daIZ/rGEHGVM5uMbYXqq8HaWbtoZhKXAQEBAgB4XACA1vOr/lbcBdXWiGf6xhBxlTObjG2F6qvB2lm7aGYAAABuMGwGCSqGSIb3DQEHBqBfMF0CAQAwWAYJKoZIhvcNAQcBMB4GCWCGSAFlAwQBLjARBAwUuYBc9YjGGlPjGZQCARCAK1BnG02jRgCbcUdxEB902q5pFMiOvEFMwOyNKeieCZ1TEhy5H8yzfRFpm2g=')
    def test_search_with_wrong_creds(self):
        with mock.patch.dict(the_price.search_engine.amazon_price_finder.os.environ, {'AMAZON_ACCESS_KEY': 'test',
                                                                           'AMAZON_SECRET_KEY': 'test',
                                                                           'AMAZON_ASSOC_TAG' : 'test'}):
            finder = AmazonPriceFinder()
            try:
                finder.find('kindle')
                self.fail()
            except Exception as ex:
                # expect a HTTP or Cipher Error
                self.assertIsInstance(ex, Exception)

    # right credential should be loaded from env variables
    def test_search_with_right_creds(self):
        finder = AmazonPriceFinder()
        title, price, currency = finder.find('kindle')
        self.assertIsNotNone(title)
        self.assertIsNotNone(price)
        self.assertIsNotNone(currency)

