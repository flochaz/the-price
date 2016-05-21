from googleapiclient.discovery import build
import os
import pprint

class GooglePriceFinder(object):
    ''' Search for price on Amazon using product api. '''

    def __init__(self):
        """
        Set creds from env variables. Raise KeyError exception if any env var not found
        """
        self.name = 'Google'
        global GOOGLE_DEVELOPER_KEY
        global GOOGLE_CUSTOM_SEARCH_ENGINE_KEY
        try:
            GOOGLE_DEVELOPER_KEY = os.environ['GOOGLE_DEVELOPER_KEY']
            GOOGLE_CUSTOM_SEARCH_ENGINE_KEY = os.environ['GOOGLE_CUSTOM_SEARCH_ENGINE_KEY']
        except KeyError as e:
            raise e

    def find(self, item):
        service = build("customsearch", "v1",
            developerKey=GOOGLE_DEVELOPER_KEY)

        response = service.cse().list(
        q='how much is the kobe bryant newport beach house ?',
        cx=GOOGLE_CUSTOM_SEARCH_ENGINE_KEY,
        ).execute()
        pprint.pprint(response['items'][0]['pagemap']['metatags'][0]['og:description'])
        return response