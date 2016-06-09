from amazon.api import AmazonAPI
from the_price.utils import logger, creds_parser

from the_price.search_engines.price_finder import PriceFinder, ItemNotFoundException

log = logger.get_logger(__name__)


class AmazonPriceFinder(PriceFinder):
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


        global amazon_access_key, amazon_secret_key, amazon_assoc_tag

        creds = creds_parser.get_creds(self.name)
        amazon_access_key = creds['amazon_access_key']
        amazon_secret_key = creds['amazon_secret_key']
        amazon_assoc_tag = creds['amazon_assoc_tag']


    def find(self, item):
        """
        :param item: item to search
        :return: title from vendor, price, currency . Raise a amazon.api.SearchException if nothing found
        """
        log.info('search for {item} through {class_name}'.format(item=item, class_name=__name__))
        try:
            amazon = AmazonAPI(amazon_access_key, amazon_secret_key, amazon_assoc_tag)
            products = amazon.search_n( 1, Keywords=item, SearchIndex='All')

            title = products[0].title
            price, currency = products[0].list_price
            log.info('Found price for {title}'.format(title=title))

            return title, price, currency
        #TODO identify proper
        except Exception as e:
            log.error(e.message)
            raise ItemNotFoundException