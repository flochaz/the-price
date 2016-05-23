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


  