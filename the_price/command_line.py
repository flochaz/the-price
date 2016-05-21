import click

from the_price.search_engine.price_finder import PriceFinder


@click.command()
@click.argument('item', type=click.STRING)
@click.option('--shop', help='Narrow done the search to a specific shop')
def ask_the_price_of(item, shop):
    """Main function to get the price of an item from a specific shop.
    If no shop provided, default strategy will apply"""
    price_finder = PriceFinder()
    title, price, currency = price_finder.find(item)
    click.echo(title + ' cost ' +  str(price) + ' ' + currency + ' on ' + price_finder.name)