import unittest
from mock import patch

from the_price.interfaces import voice_control
from the_price.utils.creds_parser import get_creds
from amazon.api import SearchException


class TestVoiceControl(unittest.TestCase):

    def test_launch_request_route_to_welcome(self):
        request = {
          "session": {
            "application": {
            "applicationId": get_creds('Alexa').get('alexa_application_id')
            }
          },
          "request": {
            "type": "LaunchRequest"
          },
          "version": "1.0"
        }
        response = voice_control.lambda_handler(request)

        self.assertEqual(response['response']['outputSpeech']['text'], voice_control.WELCOME_MSG)
        self.assertFalse(response['response']['shouldEndSession'])
        self.assertEqual(response['response']['reprompt']['outputSpeech']['text'], voice_control.REPROMPT_MSG)




    def test_end_session_request_route_to_end(self):
        request = {
          "session": {
            "application": {
            "applicationId": get_creds('Alexa').get('alexa_application_id')
            }
          },
          "request": {
            "type": "SessionEndedRequest"
          },
          "version": "1.0"
        }
        response = voice_control.lambda_handler(request)

        self.assertEqual(response['response']['outputSpeech']['text'], voice_control.END_MSG)
        self.assertTrue(response['response']['shouldEndSession'])


    def test_help_intent_request_route_to_reprompt(self):
        request = {
          "session": {
            "application": {
            "applicationId": get_creds('Alexa').get('alexa_application_id')
            }
          },
          "request": {
            "type": "IntentRequest",
            "requestId": "EdwRequestId.MY_UUID",
            "timestamp": "2016-05-22T18:36:12Z",
            "intent": {
              "name": "AMAZON.HelpIntent"
            },
            "locale": "en-US"
          },
          "version": "1.0"
        }

        response = voice_control.lambda_handler(request)
        self.assertEqual(response['response']['outputSpeech']['text'], voice_control.REPROMPT_MSG)
        self.assertEqual(response['response']['reprompt']['outputSpeech']['text'], voice_control.REPROMPT_MSG)
        self.assertFalse(response['response']['shouldEndSession'])


    def test_cancel_intent_request_route_to_end(self):
        request = {
          "session": {
            "application": {
            "applicationId": get_creds('Alexa').get('alexa_application_id')
            }
          },
          "request": {
            "type": "IntentRequest",
            "requestId": "EdwRequestId.MY_UUID",
            "timestamp": "2016-05-22T18:36:12Z",
            "intent": {
              "name": "AMAZON.CancelIntent"
            },
            "locale": "en-US"
          },
          "version": "1.0"
        }

        response = voice_control.lambda_handler(request)
        self.assertEqual(response['response']['outputSpeech']['text'], voice_control.END_MSG)
        self.assertTrue(response['response']['shouldEndSession'])

    def test_stop_intent_request_route_to_end(self):
        request = {
          "session": {
            "application": {
            "applicationId": get_creds('Alexa').get('alexa_application_id')
            }
          },
          "request": {
            "type": "IntentRequest",
            "requestId": "EdwRequestId.MY_UUID",
            "timestamp": "2016-05-22T18:36:12Z",
            "intent": {
              "name": "AMAZON.StopIntent"
            },
            "locale": "en-US"
          },
          "version": "1.0"
        }

        response = voice_control.lambda_handler(request)
        self.assertEqual(response['response']['outputSpeech']['text'], voice_control.END_MSG)
        self.assertTrue(response['response']['shouldEndSession'])

    def test_unknown_intent_request_route_to_default(self):
        request = {
          "session": {
            "application": {
            "applicationId": get_creds('Alexa').get('alexa_application_id')
            }
          },
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
        self.assertEqual(response['response']['outputSpeech']['text'], voice_control.UNKNOWN_MSG + voice_control.REPROMPT_MSG)
        self.assertFalse(response['response']['shouldEndSession'])


    @patch('the_price.search_engines.amazon_price_finder.AmazonPriceFinder.find')
    def test_get_existing_item(self, find):
        item = 'kindle'
        price = '119'
        currency = 'USD'
        find.return_value = 'kindle', price, currency
        request = {
          "session": {
            "application": {
            "applicationId": get_creds('Alexa').get('alexa_application_id')
            }
          },
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
        self.assertFalse(response['response']['shouldEndSession'])

    @patch('the_price.interfaces.command_line.SearchEngine.find')
    def test_get_not_existing_item(self, find):
        find.side_effect = SearchException()
        request = {
          "session": {
            "application": {
            "applicationId": get_creds('Alexa').get('alexa_application_id')
            }
          },
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
        self.assertEqual(response['response']['outputSpeech']['text'], voice_control.NOT_FOUND_MSG + '. ' + voice_control.CONTINUE_MSG)
        self.assertFalse(response['response']['shouldEndSession'])



    @patch('the_price.interfaces.command_line.SearchEngine.find')
    def test_get_none_item(self, find):
        request = {
          "session": {
            "application": {
            "applicationId": get_creds('Alexa').get('alexa_application_id')
            }
          },
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
