"""
In this file we specify default event handlers which are then populated into the handler map using metaprogramming
"""

from ask import alexa
from the_price.search_engines.search_engine import SearchEngine

WELCOME_MSG = "Hello Welcome to How much !"
REPROMPT_MSG = "Ask me for the price of anything you have in mind by asking: How much is it ?"
END_MSG = "Goodbye!"
UNKNOWN_MSG = "Sorry, I didn't get what you said ..."
NOT_FOUND_MSG = "Sorry, I could not find the answer."

def lambda_handler(request_obj, context=None):

    metadata = {} # add metadata to the request using key value pairs

    return alexa.route_request(request_obj, metadata)


@alexa.default_handler()
def default_handler(request):
    """ The default handler gets invoked if no handler is set for a request type """
    return alexa.create_response(message=REPROMPT_MSG)


@alexa.request_handler("LaunchRequest")
def launch_request_handler(request):
    ''' Handler for LaunchRequest '''
    return alexa.create_response(message=WELCOME_MSG)


@alexa.request_handler("SessionEndedRequest")
def session_ended_request_handler(request):
    return alexa.create_response(message=END_MSG)


@alexa.intent_handler('GetItemPriceIntent')
def get_item_price_intent_handler(request):
    """
    You can insert arbitrary business logic code here
    """

    # Get variables like userId, slots, intent name etc from the 'Request' object
    item = request.slots["Item"]  # Gets an Item Slot from the Request object.

    if item == None:
        return alexa.create_response(UNKNOWN_MSG)

    try:
        search_engine = SearchEngine()
        title, price, currency = search_engine.find(item)
        response = item + ' seems to worth ' +  str(price) + ' ' + currency + ' according to ' + search_engine.finder.name
    except:
        return alexa.create_response(NOT_FOUND_MSG)

    # alexa can also build cards which can be sent as part of the response
    card = alexa.create_card(title="GetItemPriceIntent " + item, subtitle=None,
                             content=response)

    return alexa.create_response(response,
                                 end_session=True, card_obj=card)