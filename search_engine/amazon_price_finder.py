from amazon.api import AmazonAPI
import os


class AmazonPriceFinder(object):
    ''' Search for price on Amazon using product api. '''

    def __init__(self):
        """
        Set creds from env variables. Raise KeyError exception if any env var not found
        """
        self.name = 'Amazon'
        # Setup creds from env variables
        global AMAZON_ACCESS_KEY
        global AMAZON_SECRET_KEY
        global AMAZON_ASSOC_TAG
        try:
            AMAZON_ACCESS_KEY = os.environ['AMAZON_ACCESS_KEY']
            AMAZON_SECRET_KEY = os.environ['AMAZON_SECRET_KEY']
            AMAZON_ASSOC_TAG = os.environ['AMAZON_ASSOC_TAG']
        except KeyError as e:
            raise e

    def find(self, item):
        amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)
        print('search ' + item + ' on amazon using creds : '+ AMAZON_ACCESS_KEY)
        products = amazon.search_n( 1, Keywords=item, SearchIndex='All')
        title = products[0].title
        price, currency  = products[0].list_price
        print title + ' cost ' +  str(price) + ' ' + currency + ' on amazon'
        return title, price, currency