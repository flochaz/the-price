class PriceFinder(object):
    """
    Base object of the price finder Strategy.
    Default strategy an be changed by updated the init parameter 'strategy'
    """

    def __init__(self, target=None):
        raise NotImplementedError


    def find(self, item):
        raise NotImplementedError



class ItemNotFoundException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)
