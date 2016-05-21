import unittest
from urllib2 import HTTPError

import mock

from the_price.search_engine.amazon_price_finder import  AmazonPriceFinder
import the_price


class TestAmazonPriceFinder(unittest.TestCase):

    def test_search_with_wrong_creds(self):
        with mock.patch.dict(the_price.search_engine.amazon_price_finder.os.environ, {'AMAZON_ACCESS_KEY': 'test',
                                                                           'AMAZON_SECRET_KEY': 'test',
                                                                           'AMAZON_ASSOC_TAG' : 'test'}):
            finder = AmazonPriceFinder()
            try:
                finder.find('kindle')
            except Exception as ex:
                # expect a HTTP Error
                self.assertIsInstance(ex, HTTPError)


    # right credential should be loaded from env variables
    def test_search_with_right_creds(self):
        finder = AmazonPriceFinder()
        title, price, currency = finder.find('kindle')
        self.assertIsNotNone(title)
        self.assertIsNotNone(price)
        self.assertIsNotNone(currency)

