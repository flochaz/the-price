import unittest
from mock import patch
from the_price.search_engines.search_engine import resolv_target, SearchEngine
from the_price.search_engines.amazon_price_finder import AmazonPriceFinder
from the_price.search_engines.google_price_finder import GooglePriceFinder
import the_price

class TestResolver(unittest.TestCase):

    def test_resolv_target_with_none_given(self):
        target = resolv_target(None)
        self.assertEqual(AmazonPriceFinder, target)

    def test_resolv_target_with_other_than_default_value_given(self):
        target = resolv_target('google')
        self.assertEqual(GooglePriceFinder, target)


    def test_resolv_target_with_wrong_value_given(self):
        target = resolv_target('unkown_search_engine')
        self.assertEqual(AmazonPriceFinder, target)

class TestSearchEngine(unittest.TestCase):


    @patch('the_price.utils.utils.decrypt_data')
    def test_init_no_target(self, decrypt_data):
        decrypt_data.return_value = None
        default_finder = SearchEngine().finder
        self.assertIsNone(default_finder)

    @patch('the_price.utils.utils.decrypt_data')
    def test_init_target_google(self, decrypt_data):
        decrypt_data.return_value = None
        default_finder_name = SearchEngine('google').finder.name
        self.assertEqual('Google', default_finder_name)

    @patch('the_price.search_engines.google_price_finder.GooglePriceFinder.find')
    @patch('the_price.utils.utils.decrypt_data')
    def test_find_target_google(self, decrypt_data, google_find):
        decrypt_data.return_value = None
        SearchEngine('google').find('test')
        self.assertTrue(google_find.called)


    @patch('the_price.search_engines.google_price_finder.GooglePriceFinder.find')
    @patch('the_price.utils.utils.decrypt_data')
    def test_find_target_google(self, decrypt_data, google_find):
        decrypt_data.return_value = None
        SearchEngine('google').find('test')
        self.assertTrue(google_find.called)


    @patch('the_price.search_engines.google_price_finder.GooglePriceFinder.find')
    @patch('the_price.search_engines.amazon_price_finder.AmazonPriceFinder.find')
    @patch('the_price.utils.utils.decrypt_data')
    def test_find_no_target_result_from_first(self, decrypt_data, amazon_find, google_find):
        test_value = 'test'
        decrypt_data.return_value = None
        amazon_find.return_value = test_value, test_value, test_value
        google_find.return_value = None, None, None
        text, price, currency = SearchEngine().find('test')
        self.assertTrue(amazon_find.called)
        self.assertFalse(google_find.called)
        self.assertEqual(test_value, text)
        self.assertEqual(test_value, price)
        self.assertEqual(test_value, currency)



    @patch('the_price.search_engines.google_price_finder.GooglePriceFinder.find')
    @patch('the_price.search_engines.amazon_price_finder.AmazonPriceFinder.find')
    @patch('the_price.utils.utils.decrypt_data')
    def test_find_no_target_result_from_first(self, decrypt_data, amazon_find, google_find):
        test_value = 'test'
        decrypt_data.return_value = None
        amazon_find.return_value = None, None, None
        google_find.return_value = test_value, test_value, test_value
        text, price, currency = SearchEngine().find('test')
        self.assertTrue(amazon_find.called)
        self.assertTrue(google_find.called)
        self.assertEqual(test_value,text)
        self.assertEqual(test_value,price)
        self.assertEqual(test_value,currency)