import unittest
from amazon.api import SearchException
from click.testing import CliRunner
from mock import patch

from the_price.interfaces import command_line


class TestCLI(unittest.TestCase):

    def test_cli_help(self):
        runner = CliRunner()
        result = runner.invoke(command_line.ask_the_price_of, ['--help'])
        assert result.exit_code == 0
        assert not result.exception
        self.assertTrue('Usage' in result.output, result.output)

    @patch('the_price.search_engines.amazon_price_finder.AmazonPriceFinder.find')
    def test_cli_exiting_item_case1(self, find):
        find.return_value = 'kindle', '119', 'USD'
        find.exit_code = 0
        runner = CliRunner()
        result = runner.invoke(command_line.ask_the_price_of, ['kindle'])
        assert result.exit_code == 0
        assert not result.exception
        self.assertTrue('kindle cost 119 USD on Amazon' in result.output, result.output)

    @patch('the_price.search_engines.amazon_price_finder.AmazonPriceFinder.find')
    @patch('the_price.search_engines.google_price_finder.GooglePriceFinder.find')
    def test_cli_exiting_item_case2(self, find_google, find_amazon):
        find_amazon.return_value = None, None, None
        find_google.return_value = 'tesla', '350000', 'USD'
        runner = CliRunner()
        result = runner.invoke(command_line.ask_the_price_of, ['tesla'])
        assert result.exit_code == 0
        assert not result.exception
        self.assertTrue('tesla cost 350000 USD on Google' in result.output, result.output)

    @patch('the_price.interfaces.command_line.SearchEngine.find')
    def test_cli_exiting_item_google(self, find):
        find.return_value = 'kindle', '119', 'USD'
        find.exit_code = 0
        runner = CliRunner()
        result = runner.invoke(command_line.ask_the_price_of, ['kindle','--shop','google'])
        assert result.exit_code == 0
        assert not result.exception
        self.assertTrue('kindle cost 119 USD on Google' in result.output, result.output)


    @patch('the_price.interfaces.command_line.SearchEngine.find')
    def test_cli_exiting_item_unknown(self, find):
        find.return_value = 'kindle', '119', 'USD'
        find.exit_code = 0
        runner = CliRunner()
        result = runner.invoke(command_line.ask_the_price_of, ['kindle','--shop','wretrytuy'])
        assert result.exit_code == 0
        assert not result.exception
        self.assertTrue('kindle cost 119 USD on Amazon' in result.output, result.output)

    @patch('the_price.interfaces.command_line.SearchEngine.find')
    def test_cli_not_existing_item(self, find):
        find.side_effect = SearchException()
        runner = CliRunner()
        result = runner.invoke(command_line.ask_the_price_of, ['qwertyui'])
        assert result.exit_code == 0
        assert not result.exception
        self.assertTrue('Item not found' in result.output, result.output)