import unittest
from mock import patch

from the_price.interfaces import voice_control

class TestVoiceControl(unittest.TestCase):

    #TODO: check find not called
    def test_launch_request_route_to_welcome(self):
        request = {
          "request": {
            "type": "LaunchRequest"
          },
          "version": "1.0"
        }
        response = voice_control.lambda_handler(request)

        self.assertEqual(response['response']['outputSpeech']['text'], voice_control.WELCOME_MSG)


    #TODO: check find not called
    def test_end_session_request_route_to_end(self):
        request = {
          "request": {
            "type": "SessionEndedRequest"
          },
          "version": "1.0"
        }
        response = voice_control.lambda_handler(request)

        self.assertEqual(response['response']['outputSpeech']['text'], voice_control.END_MSG)

    #TODO: check find not called
    def test_unknown_intent_request_route_to_default(self):
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

    #TODO: Mock key decryption and search
    def test_get_existing_item(self):
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
                  "value": "kindle"
                }
              }
            },
            "locale": "en-US"
          },
          "version": "1.0"
        }

        response = voice_control.lambda_handler(request)
        self.assertTrue('cost' in response['response']['outputSpeech']['text'])
        self.assertEqual(response['response']['card']['content'],voice_control.CARD_MSG)

    #TODO: Mock key decryption and search
    def test_get_not_existing_item(self):
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


    #TODO: Mock key decryption and search
    def test_get_none_item(self):
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
