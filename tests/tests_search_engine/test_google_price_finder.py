import unittest
from mock import patch


from the_price.search_engines.google_price_finder import  GooglePriceFinder, creds_parser
from the_price.search_engines.google_price_finder import extract_price_from_text


class TestGooglePriceFinder(unittest.TestCase):

    @patch('the_price.utils.creds_parser.get_creds')
    def test_search_with_wrong_creds(self, fake_get_creds):
        fake_get_creds.return_value = {'google_custom_search_engine_key': 'fake_key',
                                       'google_developer_key': 'fake_key'}
        finder = GooglePriceFinder()
        try:
            finder.find('kindle')
            self.fail()
        except Exception as ex:
            # expect a InvalidCiphertextException
            self.assertIsInstance(ex, Exception)

    def test_search_with_right_creds(self):
        finder = GooglePriceFinder()
        items = [{'item': 'us debt',
                     'price': '19,012,827,698,418',
                     'currency': '$'},
                 {'item': 'kobe bryant newport beach house',
                     'price': '6.1 million',
                     'currency': '$'},
                    {'item': 'tesla model 3 in $',
                     'price': '35,000',
                     'currency': '$'},
                    {'item': 'tesla model S',
                     'price': '71,500',
                     'currency': '$'},
                 {'item': 'kindle Fire',
                     'price': '50',
                     'currency': '$'},
                 {'item': 'DJI Phantom 3',
                  'price': '499',
                  'currency' : '$'}]
        for item in items:
            text, price, currency = finder.find(item['item'])
            self.assertEqual(item['price'], price)
            self.assertEqual(item['currency'], currency)

    def test_search_no_existing_item(self):
        try:
            finder = GooglePriceFinder()
            finder.find('bdgjudmymhrdm')
            self.fail()
        except Exception as ex:
            self.assertIsInstance(ex, Exception)


    def test_extract_price_from_text(self):
        to_test = {'$6.1 million', '$6.1 m', '$0.61 M', '$6 billion','$35,000', '$35000', '$35,000.00', '$ 35000'}

        self.price_tester('$6 million', '$', '6 million')
        self.price_tester('$6.1 billion', '$', '6.1 billion')
        self.price_tester('$6 trillion', '$', '6 trillion')
        self.price_tester('6.2 trillion euros', 'euros', '6.2 trillion')
        self.price_tester('6 trillion euros', 'euros', '6 trillion')
        self.price_tester('$35,000', '$', '35,000')
        self.price_tester('$35000', '$', '35000')
        self.price_tester('$35000.00', '$', '35000.00')
        self.price_tester('$35,000.00', '$', '35,000.00')
        self.price_tester('$19,012,827,698,418', '$', '19,012,827,698,418')




    def price_tester(self, display_text, expected_currency, expected_price):
        description = "The price is {display_text} bla bla bla".format(display_text=display_text)

        text, price, currency = extract_price_from_text(description)

        self.assertEqual(expected_price, price)
        self.assertEqual(expected_currency, currency)