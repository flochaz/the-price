#!/usr/bin/python
# -*- coding: UTF8 -*-

from googleapiclient.discovery import build
import pprint
from the_price.utils import utils
import base64
import re

from the_price.search_engines.price_finder import PriceFinder

ENCRYPTED_GOOGLE_DEVELOPER_KEY='CiBcAIDW86v+VtwF1daIZ/rGEHGVM5uMbYXqq8HaWbtoZhKvAQEBAgB4XACA1vOr/lbcBdXWiGf6xhBxlTObjG2F6qvB2lm7aGYAAACGMIGDBgkqhkiG9w0BBwagdjB0AgEAMG8GCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMewGXR5nRnAhvG+V7AgEQgEJw8+MnUI02rDomatA2NSZa7DBmKG8hCUwbIsxx4m7OkTvOEa4XqNnqzo4ryhGYzbAPK7iwDnCk6iaLvBv3Q96TGWM='
ENCRYPTED_GOOGLE_CUSTOM_SEARCH_ENGINE_KEY='CiBcAIDW86v+VtwF1daIZ/rGEHGVM5uMbYXqq8HaWbtoZhKoAQEBAgB4XACA1vOr/lbcBdXWiGf6xhBxlTObjG2F6qvB2lm7aGYAAAB/MH0GCSqGSIb3DQEHBqBwMG4CAQAwaQYJKoZIhvcNAQcBMB4GCWCGSAFlAwQBLjARBAyR114xwTWYi7LVqpICARCAPBRadBmFoyLKzLYGeEHei0dwuTcn1C9jy8NM22rOMRN0RYcXMx/12cmgDzq58bZqO1/u3e+8BK7AIo7pzA=='


class GooglePriceFinder(PriceFinder):
    ''' Search for price on Google using custom search api. '''

    def __init__(self):
        """
        Set creds from env variables. Raise KeyError exception if any env var not found
        """
        self.name = 'Google'
        global GOOGLE_DEVELOPER_KEY
        global GOOGLE_CUSTOM_SEARCH_ENGINE_KEY

        GOOGLE_DEVELOPER_KEY = utils.decrypt_data(base64.b64decode(ENCRYPTED_GOOGLE_DEVELOPER_KEY))
        GOOGLE_CUSTOM_SEARCH_ENGINE_KEY = utils.decrypt_data(base64.b64decode(ENCRYPTED_GOOGLE_CUSTOM_SEARCH_ENGINE_KEY))


    #TODO: Refactor !!
    def find(self, item):
        service = build("customsearch", "v1",
            developerKey=GOOGLE_DEVELOPER_KEY)
        #https://developers.google.com/custom-search/json-api/v1/reference/cse/list#response
        response = service.cse().list(
        q='how much is the ' + item,
        cx=GOOGLE_CUSTOM_SEARCH_ENGINE_KEY,
        ).execute()
        currency, price = None, None
        check_items = 0
        while check_items < 9 and (not currency or not price):

            if 'pagemap' in response['items'][check_items] and\
                            'metatags' in response['items'][check_items]['pagemap'] and \
                            'og:description' in response['items'][check_items]['pagemap']['metatags'][0] and not price:
                original_description, price, currency = extract_price_from_text(
                    response['items'][check_items]['pagemap']['metatags'][0]['og:description'])
            check_items += 1

        # If nothing found through description then search through snippet
        check_items = 0
        while check_items < 10 and (not currency or not price):
            print 'CHECK htmlSnippet'
            original_description, price, currency = extract_price_from_text(response['items'][check_items]['htmlSnippet'])
            pprint.pprint(original_description)

            if not price:
                print 'CHECK Snippet'
                original_description, price, currency = extract_price_from_text(response['items'][check_items]['snippet'])
                pprint.pprint(original_description)
            check_items += 1
        print 'RETURN WHAT ?'
        return original_description, price, currency



def extract_price_from_text(original_description):
    price, currency = None, None
    match = re.search(ur'([£$€])(\d+(?:\,\d{3}){0,10}(?:\.\d{1,2})?(?:\ (?:million|billion|trillion))?)',
                      original_description)
    if not match:
        match = re.search(ur'(\d+(?:\.\d{0,2})?(?:\ (?:million|billion|trillion))?)\ ((?:dollars|pounds|euros|USD|GBP|EUR))',
                          original_description)
        if match:
            price, currency = match.groups()
    else:
        currency, price = match.groups()

    return original_description, price, currency