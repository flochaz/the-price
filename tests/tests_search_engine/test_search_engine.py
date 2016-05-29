import unittest
from mock import patch
from the_price.search_engines.search_engine import resolv_strategy, SearchEngine
from the_price.search_engines.amazon_price_finder import AmazonPriceFinder
from the_price.search_engines.google_price_finder import GooglePriceFinder


class TestResolver(unittest.TestCase):

    def test_resolv_target_with_none_given(self):
        target = resolv_strategy(None)
        self.assertEqual(AmazonPriceFinder, target)

    def test_resolv_target_with_other_than_default_value_given(self):
        target = resolv_strategy('google')
        self.assertEqual(GooglePriceFinder, target)


    def test_resolv_target_with_wrong_value_given(self):
        target = resolv_strategy('unkown_search_engine')
        self.assertEqual(AmazonPriceFinder, target)


    @patch('the_price.utils.utils.decrypt_data')
    def test_init_no_target(self, decrypt_data):
        decrypt_data.return_value = None
        default_finder_name = SearchEngine().finder.name
        self.assertEqual('Amazon', default_finder_name)

    @patch('the_price.utils.utils.decrypt_data')
    def test_init_target_google(self, decrypt_data):
        decrypt_data.return_value = None
        default_finder_name = SearchEngine('google').finder.name
        self.assertEqual('Google', default_finder_name)


