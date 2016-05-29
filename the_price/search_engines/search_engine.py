
import sys, inspect
from the_price.search_engines.price_finder import PriceFinder
from the_price.search_engines.amazon_price_finder import AmazonPriceFinder
# Following import only needed to make the __subclasses__() function to return that one as well ...
from the_price.search_engines.google_price_finder import GooglePriceFinder


class SearchEngine(object):

    def __init__(self, target='amazon'):
        if not target:
            target = 'amazon'
        resolved_target = resolv_strategy(target)
        self.finder = resolved_target()
        self.name = self.finder.name

    def find(self, item):
        return self.finder.find(item)









def resolv_strategy(target):
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