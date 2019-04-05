from unittest import TestCase, main
from babel.localedata import locale_identifiers
import locale
import os
import requests
import json
from dotenv import load_dotenv
from main import CurrencyConverter


class TestAPI(TestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv()
        ACCES_KEY = os.getenv('ACCES_KEY')
        cls.req = requests.get('http://data.fixer.io/api/latest', params={'access_key':ACCES_KEY})
        cls.r = json.loads(cls.req.text)

    def test_connection_API(self):
        self.assertEqual(self.req.status_code, 200)

    def test_symbols_match(self):
        locale_currency_code = []
        for name in locale_identifiers():
            locale.setlocale(locale.LC_ALL, name)
            d = locale.localeconv()
            if d['int_curr_symbol'] not in locale_currency_code:
                locale_currency_code.append(d['int_curr_symbol'])
        self.assertEqual(
            {3},
            set([len(x) for x in self.r.get('rates').keys()]),
        )

    @classmethod
    def tearDownClass(cls):
        pass


class TestCurrencyConverter(TestCase):
    def test_good_connection(self):
        load_dotenv()
        ACCES_KEY = os.getenv('ACCES_KEY')
        req = requests.get('http://data.fixer.io/api/latest', params={'access_key':ACCES_KEY})
        r = json.loads(req.text)
        self.assertEqual(r['success'], True)

    def test_bad_connection(self):
        ACCES_KEY = 'Bad acces key'
        req = requests.get('http://data.fixer.io/api/latest', params={'access_key':ACCES_KEY})
        r = json.loads(req.text)
        self.assertEqual(r['success'], False)

    def test_connection_application(self):
        ACCES_KEY = os.getenv('ACCES_KEY')
        a = CurrencyConverter(api_url='http://data.fixer.io/api/latest', api_params={'access_key': ACCES_KEY})
        self.assertEqual(a.req.status_code, 200)
        self.assertEqual(a.r['success'], True)

# mock this
    # def test_currency_convert(self):
    #     a = CurrencyConverter(api_url='http://data.fixer.io/api/latest', api_params={'access_key': ACCES_KEY})
    #     a.convert(10, "EUR", "PLN"))


if __name__ == '__main__':
    main()