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


    def test_init_no_target(self):
        default_finder = SearchEngine().finder
        self.assertIsNone(default_finder)

    def test_init_target_google(self):
        default_finder_name = SearchEngine('google').finder.name
        self.assertEqual('Google', default_finder_name)

    @patch('the_price.search_engines.google_price_finder.GooglePriceFinder.find')
    def test_find_target_google(self, google_find):
        SearchEngine('google').find('test')
        self.assertTrue(google_find.called)


    @patch('the_price.search_engines.google_price_finder.GooglePriceFinder.find')
    def test_find_target_google(self, google_find):
        SearchEngine('google').find('test')
        self.assertTrue(google_find.called)


    @patch('the_price.search_engines.google_price_finder.GooglePriceFinder.find')
    @patch('the_price.search_engines.amazon_price_finder.AmazonPriceFinder.find')
    def test_find_no_target_result_from_first(self, amazon_find, google_find):
        test_value = 'test'
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
    def test_find_no_target_result_from_first(self, amazon_find, google_find):
        test_value = 'test'
        amazon_find.return_value = None, None, None
        google_find.return_value = test_value, test_value, test_value
        text, price, currency = SearchEngine().find('test')
        self.assertTrue(amazon_find.called)
        self.assertTrue(google_find.called)
        self.assertEqual(test_value,text)
        self.assertEqual(test_value,price)
        self.assertEqual(test_value,currency)