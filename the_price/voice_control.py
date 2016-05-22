"""
In this file we specify default event handlers which are then populated into the handler map using metaprogramming
"""

from ask import alexa
from the_price.search_engine.price_finder import PriceFinder


def lambda_handler(request_obj, context=None):

    metadata = {} # add metadata to the request using key value pairs

    return alexa.route_request(request_obj, metadata)


@alexa.default_handler()
def default_handler(request):
    """ The default handler gets invoked if no handler is set for a request type """
    return alexa.create_response(message="Just ask")


@alexa.request_handler("LaunchRequest")
def launch_request_handler(request):
    ''' Handler for LaunchRequest '''
    return alexa.create_response(message="Hello Welcome to The Price!")


@alexa.request_handler("SessionEndedRequest")
def session_ended_request_handler(request):
    return alexa.create_response(message="Goodbye!")


@alexa.intent_handler('GetItemPriceIntent')
def get_item_price_intent_handler(request):
    """
    You can insert arbitrary business logic code here
    """

    # Get variables like userId, slots, intent name etc from the 'Request' object
    item = request.slots["Item"]  # Gets an Item Slot from the Request object.

    if item == None:
        return alexa.create_response("Could not find this item!")


    price_finder = PriceFinder()
    title, price, currency = price_finder.find(item)
    response = title + ' cost ' +  str(price) + ' ' + currency + ' on ' + price_finder.name

    # All manipulations to the request's session object are automatically reflected in the request returned to Amazon.
    # For e.g. This statement adds a new session attribute (automatically returned with the response) storing the
    # Last seen item value in the 'last_item' key.

    # request.session['last_item'] = item # Automatically returned as a sessionAttribute

    # Modifying state like this saves us from explicitly having to return Session objects after every response

    # alexa can also build cards which can be sent as part of the response
    card = alexa.create_card(title="GetItemPriceIntent activated", subtitle=None,
                             content="asked alexa to find the price of {}".format(item))

    return alexa.create_response(response,
                                 end_session=False, card_obj=card)