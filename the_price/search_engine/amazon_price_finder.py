from amazon.api import AmazonAPI

from the_price.utils import utils
import base64
import os

ENCRYPTED_AMAZON_ACCESS_KEY='CiBcAIDW86v+VtwF1daIZ/rGEHGVM5uMbYXqq8HaWbtoZhKbAQEBAgB4XACA1vOr/lbcBdXWiGf6xhBxlTObjG2F6qvB2lm7aGYAAAByMHAGCSqGSIb3DQEHBqBjMGECAQAwXAYJKoZIhvcNAQcBMB4GCWCGSAFlAwQBLjARBAwmncVuuLId80GkOzACARCAL6KWOAUtQNTZ0WLd2byRA95Mt8g/tcgPtXorhzKdC0GPXcJ2pDYMwy3ZnxKDDV8I'
ENCRYPTED_AMAZON_SECRET_KEY='CiBcAIDW86v+VtwF1daIZ/rGEHGVM5uMbYXqq8HaWbtoZhKwAQEBAgB4XACA1vOr/lbcBdXWiGf6xhBxlTObjG2F6qvB2lm7aGYAAACHMIGEBgkqhkiG9w0BBwagdzB1AgEAMHAGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMnQYaltzbBomNj7LyAgEQgEOp7hHGe3d1jsY/sl1u+NCXUJUEMYhHkQOqb2+YT6lL6/zrdQXz5auLhgmh3+vL/HtWkq18fWvrAGW5226mSoB2a+eN'
ENCRYPTED_AMAZON_ASSOC_TAG='CiBcAIDW86v+VtwF1daIZ/rGEHGVM5uMbYXqq8HaWbtoZhKXAQEBAgB4XACA1vOr/lbcBdXWiGf6xhBxlTObjG2F6qvB2lm7aGYAAABuMGwGCSqGSIb3DQEHBqBfMF0CAQAwWAYJKoZIhvcNAQcBMB4GCWCGSAFlAwQBLjARBAzzswZf3HIriQpkJ0QCARCAK1qhlINJ/ogGfczy96U/DAIQS5kFrZHVtBkW99Y6FWavQmi+5Ijv0Ei1bT8='


class AmazonPriceFinder(object):
    ''' Search for price on Amazon using product api. '''



    def __init__(self):
        """
        Set creds from env variables. Raise KeyError exception if any env var not found
        """
        self.name = 'Amazon'
        # Decipher Main AWS creds using KMS encryption mechanism
        # The process here is a bit tricky: Due to the fact Amazon Product API does not support AIM, we had to implement
        # the following step to avoid to have Main AWS creds exposed in the source code:
        # 1. Create user for travis CI and AWS Lambda
        # 2. Create a KMS encryption Key and allow travis and lambda to access it
        # 3. Add travis user creds to travis env
        # 4. Add the code to decipher the hardcoded main AWS encrypted key


        global AMAZON_ACCESS_KEY
        global AMAZON_SECRET_KEY
        global AMAZON_ASSOC_TAG
        AMAZON_ACCESS_KEY=utils.decrypt_data(base64.b64decode(ENCRYPTED_AMAZON_ACCESS_KEY))
        AMAZON_SECRET_KEY=utils.decrypt_data(base64.b64decode(ENCRYPTED_AMAZON_SECRET_KEY))
        AMAZON_ASSOC_TAG=utils.decrypt_data(base64.b64decode(ENCRYPTED_AMAZON_ASSOC_TAG))


    def find(self, item):
        """
        :param item: item to search
        :return: title from vendor, price, currency . Raise a amazon.api.SearchException if nothing found
        """
        amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)
        products = amazon.search_n( 1, Keywords=item, SearchIndex='All')

        title = products[0].title
        price, currency = products[0].list_price

        return title, price, currency