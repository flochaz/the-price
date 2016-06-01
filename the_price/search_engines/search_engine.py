from the_price.search_engines.price_finder import PriceFinder
from the_price.utils import logger


# Following imports only needed to make the __subclasses__() function to return that one as well ...
from the_price.search_engines.amazon_price_finder import AmazonPriceFinder
from the_price.search_engines.google_price_finder import GooglePriceFinder

log = logger.get_logger(__name__)


class SearchEngine(object):

    def __init__(self, target=None):
        self.finder = None
        if target:
            resolved_target = resolv_target(target)
            self.finder = resolved_target()

    def find(self, item):
        log.info('Looking for the price of {item}'.format(item=item))

        if self.finder:
            return self.finder.find(item)
        else:
            text, price, currency = None, None, None
            for price_finder_class in get_all_finders_classes():
                log.info('Find {item} with {finder}'.format(item=item, finder=price_finder_class.__name__))
                self.finder = price_finder_class()
                try:
                    text, price, currency = self.finder.find(item)
                except Exception as e:
                    log.error(e.message)
                    continue
                if price:
                    break

            return text, price, currency









def resolv_target(target):
    """
    Static function enabling to find the corresponding strategy finder to use from a user input
    :param target: user entry that needs to be linked to an existing finder
    :return: finder class name
    """
    if target:
        for price_finder_class in get_all_finders_classes():
            if target in price_finder_class.__name__.lower():
                return price_finder_class
    # if not found in previous search, return the first one. which will be Amazon since it starts with a "A"
    return PriceFinder.__subclasses__()[0]


def get_all_finders_classes():
    return PriceFinder.__subclasses__()