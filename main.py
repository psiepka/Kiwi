"""Contain Convert currecy class."""

from locale import(
    setlocale as locale_setlocale,
    LC_ALL as locale_LC_ALL,
    localeconv as locale_localeconv
)
from babel.localedata import locale_identifiers
from requests import get as req_get

class CurrencyConverter:
    """Simple class, mainly to convert currency.
    Raises:
        AttributeError -- raise when currency is missing or does not exists in out application
        ValueError -- raise when amount is not number float/integer
    Returns:
        dictonary - with input and output currency data
    """

    rates = {}

    def __init__(self, api_url, api_params):
        self.req = req_get(api_url, params=api_params)
        if self.req.status_code is not 200:
            raise ConnectionError
        if self.req.json()['success'] is not True:
            raise ConnectionRefusedError
        self.r_data = self.req.json()
        self.rates = self.r_data.get('rates')
        self.base = self.r_data.get('base')

    def convert(self, amount, input_currency, output_currency=None):
        """
        Arguments:
            amount {float} -- amount of cash to convert [required]
            input_currency {str} -- currency code or symbol [required]
            output_currency {str} -- currency code or symbol (default: {None})

        Returns:
            dict - with input and output currency data
        """

        pass_input = False
        initial_amount = amount
        input_currency = self.validate_currency(input_currency)
        pass_input = True
        if input_currency != self.base:
            amount = float(amount) / float(self.rates[input_currency])
            if output_currency:
                output_currency = self.validate_currency(output_currency)
                result = {
                    output_currency: (
                        round(float(amount) * float(self.rates[output_currency]), 2)
                    )
                }
                json_result = {
                    'input':{
                        'amount': initial_amount,
                        'currency': input_currency,
                    },
                    'output': result
                }
                return json_result
            else:
                result = {k: round(v*amount, 2) for k, v in self.rates.items()}
                json_result = {
                    'input':{
                        'amount': initial_amount,
                        'currency': input_currency,
                    },
                    'output': result
                }
                return json_result
        elif input_currency == self.base:
            result = float(amount) * float(self.rates[output_currency])
            if output_currency:
                result = {
                    output_currency: (
                        round(float(amount) * float(self.rates[output_currency]), 2)
                    )
                }
                json_result = {
                    'input':{
                        'amount': initial_amount,
                        'currency': input_currency,
                    },
                    'output': result
                }
                return json_result
            else:
                result = {k: round(v*amount, 2) for k, v in self.rates.items()}
                json_result = {
                    'input':{
                        'amount': initial_amount,
                        'currency': input_currency,
                    },
                    'output': result
                }
                return json_result


    def validate_currency(self, currency):
        """Search currency code or sign in application

        Arguments:
            currency {str} -- currecy code or sign

        Raises:
            AttributeError -- raise when currency does not exist in app

        Returns:
            [str] -- confimed currency code/sign
        """

        try:
            if len(currency) == 3:
                if currency in self.rates.keys():
                    return currency
            currency = self.search_currency_symbol(currency)
            if currency is None:
                raise AttributeError
            return currency
        except AttributeError:
            raise AttributeError({'error_message': "Currency doesn't exist"})


    @staticmethod
    def search_currency_symbol(symbol_or_sign):
        """Search currency name by currency sign

        Returns:
            str -- currency 3 letters code
        """
        for name in locale_identifiers():
            locale_setlocale(locale_LC_ALL, name)
            d = locale_localeconv()
            if d['currency_symbol'].lower() == symbol_or_sign.lower():
                return d['int_curr_symbol']
        return None
