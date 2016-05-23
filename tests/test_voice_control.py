import unittest
from mock import patch
import boto3
import json

class TestVoiceControl(unittest.TestCase):


    def test_cli_help(self):
        pass

    @patch('the_price.command_line.PriceFinder.find')
    def test_cli_exiting_item(self, find):
        pass



    @patch('the_price.command_line.PriceFinder.find')
    def test_cli_not_existing_item(self, find):
        pass


    def test_integration_with_lambda(self):
        request = {
                  "session": {
                    "sessionId": "SessionId.9a2852dd-1e2c-4974-a93f-7a06df505cbd",
                    "application": {
                      "applicationId": "amzn1.echo-sdk-ams.app.cb62f273-d576-4b6e-86fb-8929a89c4103"
                    },
                    "user": {
                      "userId": "test"
                    },
                    "new": False
                  },
                  "request": {
                    "type": "IntentRequest",
                    "requestId": "EdwRequestId.3fbdf8d0-6466-4b43-bb5a-d553cbda9af4",
                    "timestamp": "2016-05-22T18:36:12Z",
                    "intent": {
                      "name": "GetItemPriceIntent",
                      "slots": {
                        "Item": {
                          "name": "Item",
                          "value": "Kindle"
                        }
                      }
                    },
                    "locale": "en-US"
                  },
                  "version": "1.0"
                }

        lambda_client = boto3.client('lambda', region_name='us-east-1')
        response = lambda_client.invoke(FunctionName='arn:aws:lambda:us-east-1:996747011861:function:theprice', InvocationType='RequestResponse',  LogType='None', Payload=json.dumps(request))
        self.assertTrue('cost' in response['Payload'].read())