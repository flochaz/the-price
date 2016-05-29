import unittest
from mock import patch

from the_price.interfaces import voice_control
from amazon.api import SearchException


class TestVoiceControl(unittest.TestCase):

    def test_launch_request_route_to_welcome(self):
        request = {
          "request": {
            "type": "LaunchRequest"
          },
          "version": "1.0"
        }
        response = voice_control.lambda_handler(request)

        self.assertEqual(response['response']['outputSpeech']['text'], voice_control.WELCOME_MSG)


    def test_end_session_request_route_to_end(self):
        request = {
          "request": {
            "type": "SessionEndedRequest"
          },
          "version": "1.0"
        }
        response = voice_control.lambda_handler(request)

        self.assertEqual(response['response']['outputSpeech']['text'], voice_control.END_MSG)

    def test_unknown_utterance_request_route_to_default(self):
        request = {
          "request": {
            "type": "IntentRequest",
            "requestId": "EdwRequestId.MY_UUID",
            "timestamp": "2016-05-22T18:36:12Z",
            "intent": {
              "name": "UNKNOWN_INTENT",
              "slots": {
                "Item": {
                  "name": "Item",
                  "value": "kindle"
                }
              }
            },
            "locale": "en-US"
          },
          "version": "1.0"
        }

        response = voice_control.lambda_handler(request)
        self.assertEqual(response['response']['outputSpeech']['text'], voice_control.REPROMPT_MSG)

    @patch('the_price.utils.utils.decrypt_data')
    @patch('the_price.search_engines.amazon_price_finder.AmazonPriceFinder.find')
    def test_get_existing_item(self, find, decrypt_data):
        item = 'kindle'
        price = '119'
        currency = 'USD'
        decrypt_data.return_value = None
        find.return_value = 'kindle', price, currency
        request = {
          "request": {
            "type": "IntentRequest",
            "requestId": "EdwRequestId.MY_UUID",
            "timestamp": "2016-05-22T18:36:12Z",
            "intent": {
              "name": "GetItemPriceIntent",
              "slots": {
                "Item": {
                  "name": "Item",
                  "value": item
                }
              }
            },
            "locale": "en-US"
          },
          "version": "1.0"
        }

        response = voice_control.lambda_handler(request)
        self.assertTrue(item + ' seems to worth ' + price + ' ' + currency  in response['response']['outputSpeech']['text'])
        self.assertEqual(response['response']['card']['content'], response['response']['outputSpeech']['text'])

    @patch('the_price.utils.utils.decrypt_data')
    @patch('the_price.interfaces.command_line.SearchEngine.find')
    def test_get_not_existing_item(self, find, decrypt_data):
        decrypt_data.return_value = None
        find.side_effect = SearchException()
        request = {
          "request": {
            "type": "IntentRequest",
            "requestId": "EdwRequestId.MY_UUID",
            "timestamp": "2016-05-22T18:36:12Z",
            "intent": {
              "name": "GetItemPriceIntent",
              "slots": {
                "Item": {
                  "name": "Item",
                  "value": "asagdgsffgr"
                }
              }
            },
            "locale": "en-US"
          },
          "version": "1.0"
        }

        response = voice_control.lambda_handler(request)
        self.assertEqual(response['response']['outputSpeech']['text'], voice_control.NOT_FOUND_MSG)


    @patch('the_price.interfaces.command_line.SearchEngine.find')
    def test_get_none_item(self, find):
        request = {
          "request": {
            "type": "IntentRequest",
            "requestId": "EdwRequestId.MY_UUID",
            "timestamp": "2016-05-22T18:36:12Z",
            "intent": {
              "name": "GetItemPriceIntent",
              "slots": {
                "Item": {
                  "name": "Item",
                  "value": None
                }
              }
            },
            "locale": "en-US"
          },
          "version": "1.0"
        }

        response = voice_control.lambda_handler(request)
        self.assertEqual(response['response']['outputSpeech']['text'], voice_control.UNKNOWN_MSG)
        self.assertFalse(find.called)
