
@staticmethod
def resolv_strategy(shop):
    """
    Static function enabling to find the corresponding strategy finder to use from a user input
    :param shop: user entry that needs to be linked to an existing finder
    :return: finder class name
    """
    #TODO: implem introspection
    return 'AmazonPriceFinder'