import unittest
from click.testing import CliRunner
from the_price import command_line
from mock import patch
from amazon.api import SearchException


class TestCLI(unittest.TestCase):

    def test_cli_help(self):
        runner = CliRunner()
        result = runner.invoke(command_line.ask_the_price_of, ['--help'])
        assert result.exit_code == 0
        assert not result.exception
        self.assertTrue('Usage' in result.output)

    @patch('the_price.command_line.PriceFinder.find')
    def test_cli_exiting_item(self, find):
        find.return_value = 'kindle', '119', 'USD'
        runner = CliRunner()
        result = runner.invoke(command_line.ask_the_price_of, ['kindle'])
        assert result.exit_code == 0
        assert not result.exception
        self.assertTrue('kindle cost 119 USD on Amazon' in result.output)



    @patch('the_price.command_line.PriceFinder.find')
    def test_cli_not_existing_item(self, find):
        find.side_effect = SearchException()
        runner = CliRunner()
        result = runner.invoke(command_line.ask_the_price_of, ['qwertyui'])
        assert result.exit_code == 0
        assert not result.exception
        self.assertTrue('Item not found' in result.output)