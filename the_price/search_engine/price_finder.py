from google_price_finder import GooglePriceFinder
from  amazon_price_finder import AmazonPriceFinder

class PriceFinder(object):
    """
    Base object of the price finder Strategy.
    Default strategy an be changed by updated the init parameter 'strategy'
    """

    def __init__(self, strategy=AmazonPriceFinder):
        self.finder = None
        self.name = None
        if strategy:
            self.finder = strategy()
            self.name = self.finder.name

    def find(self, item):
        if(self.finder):
            return self.finder.find(item)
        else:
            raise UnboundLocalError('Exception raised, no strategyClass supplied to PriceFinder!')
