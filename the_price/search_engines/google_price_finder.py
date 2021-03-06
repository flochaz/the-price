#!/usr/bin/python
# -*- coding: utf-8 -*-

from googleapiclient.discovery import build
from the_price.utils import logger, creds_parser
import re

from the_price.search_engines.price_finder import PriceFinder, ItemNotFoundException

log = logger.get_logger(__name__)


class GooglePriceFinder(PriceFinder):
    ''' Search for price on Google using custom search api. '''


    def __init__(self):
        """
        Set creds from env variables. Raise KeyError exception if any env var not found
        """
        self.name = 'Google'
        global google_developer_key, google_custom_search_engine_key

        creds = creds_parser.get_creds(self.name)
        google_developer_key = creds['google_developer_key']
        google_custom_search_engine_key = creds['google_custom_search_engine_key']


    def find(self, item):
        try:
            log.info('search for {item} through {class_name}'.format(item=item, class_name=__name__))
            service = build("customsearch", "v1",
                developerKey=google_developer_key)
            #https://developers.google.com/custom-search/json-api/v1/reference/cse/list#response
            response = service.cse().list(
            q='how much is the ' + item,
            cx=google_custom_search_engine_key,
            ).execute()
            #log.debug('RESPONSE = {response}'.format(pprint.pprint(response)))
            original_description, price, currency = parse_response(response)
            return original_description, price, currency

        #TODO identify proper Exception to expect
        except Exception as e:
            log.error(e)


def parse_response(response):
    original_description, price, currency = parse_description_tag(response)

    # If nothing found through description then search through snippet
    if not price:
        original_description, price, currency = parse_snippets_tag(response)

    if not price:
        raise ItemNotFoundException

    log.debug('Price found in {desc}'.format(desc=original_description.encode('ascii', 'ignore')))

    return original_description, price, currency


def parse_description_tag(response):
    """
    Parse the pagemap/metatags/0/description of the response
    :param response: entire json
    :return: original_description, price, currency . None, None, None if nothing found
    """
    original_description, price, currency = None, None, None
    try:
        check_items = 0

        while check_items < 10 and (not currency or not price):
            if 'pagemap' in response['items'][check_items] and\
                            'metatags' in response['items'][check_items]['pagemap'] and \
                            'og:description' in response['items'][check_items]['pagemap']['metatags'][0] and not price:
                original_description, price, currency = extract_price_from_text(
                    response['items'][check_items]['pagemap']['metatags'][0]['og:description'])
            check_items += 1
    except:
        log.error('Error while parsing description tag')
    return original_description, price, currency


def parse_snippets_tag(response):
    """
    Parse the htmlSnippet and snippet tags of the response
    :param response: entire json
    :return: original_description, price, currency . None, None, None if nothing found
    """
    original_description, price, currency = None, None, None
    try:

        check_items = 0
        while check_items < 10 and (not currency or not price):
            log.debug('CHECK htmlSnippet')
            original_description, price, currency = extract_price_from_text(response['items'][check_items]['htmlSnippet'])
            log.debug(original_description.encode('ascii', 'ignore'))

            if not price:
                log.debug('CHECK Snippet')
                original_description, price, currency = extract_price_from_text(response['items'][check_items]['snippet'])
                log.debug(original_description.encode('ascii', 'ignore'))
            check_items += 1
    except:
        log.error('Error while parsing snippet tag')

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