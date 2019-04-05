#!/usr/bin/env python3
"""Command line application, which convert current currency."""

from os import getenv
from dotenv import load_dotenv
from click import command as click_command, option as click_option
from json import dumps
from main import CurrencyConverter


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
load_dotenv()
ACCES_KEY = getenv('ACCES_KEY')

@click_command(context_settings=CONTEXT_SETTINGS)
@click_option(
    '--amount', help='amount - [float/integer] Amount which we want to convert.',
    required=True, type=float
)
@click_option(
    '--input_currency', help='input_currency - [string] Input currency - 3 letters name or currency symbol.',
    required=True, type=str
)
@click_option(
    '--output_currency', default=None,
    help='output_currency - Requested/output currency - [string] 3 letters name or currency symbol.',
    required=False, type=str
)
def convert(amount, input_currency, output_currency):
    """
    Simple program that convert currency
    """
    try:
        app = CurrencyConverter(
            api_url='http://data.fixer.io/api/latest', api_params={'access_key': ACCES_KEY}
        )
        return print(dumps(app.convert(amount, input_currency, output_currency,)))
    except AttributeError as e:
        return print(dumps(e.args[0]))

if __name__ == '__main__':
    convert()
