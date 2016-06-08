import unittest
from the_price.utils.creds_parser import get_creds

class test_creds_parser(unittest.TestCase):

    def test_parse_amazon_creds(self):
        creds = get_creds('Amazon')
        print creds
        self.assertIsNotNone(creds['amazon_access_key'])
        self.assertIsNotNone(creds['amazon_secret_key'])
        self.assertIsNotNone(creds['amazon_assoc_id'])

    def test_parse_amazon_creds(self):
        creds = get_creds('Google')
        self.assertIsNotNone(creds['google_developer_key'])
        self.assertIsNotNone(creds['google_custom_search_engine_key'])