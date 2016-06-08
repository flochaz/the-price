import unittest
from the_price.search_engines.price_finder import ItemNotFoundException

from mock import  patch

from the_price.search_engines.amazon_price_finder import  AmazonPriceFinder


class TestAmazonPriceFinder(unittest.TestCase):

    @patch('the_price.utils.creds_parser.get_creds')
    def test_search_with_wrong_creds(self, fake_get_creds):
        fake_get_creds.return_value = {'amazon_access_key': 'fake_key',
                                       'amazon_secret_key': 'fake_key',
                                       'amazon_assoc_tag': 'fake_key'}

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
            self.assertIsInstance(ex, ItemNotFoundException)

