from unittest import TestCase, main
from os import getenv
from requests import get as requests_get
from dotenv import load_dotenv
from json import dumps
import requests_mock
from click.testing import CliRunner
from main import CurrencyConverter
from web_app import app
from currency_converter import convert as cli_convert


class TestAPI(TestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv()
        ACCES_KEY = getenv('ACCES_KEY')
        cls.req = requests_get('http://data.fixer.io/api/latest', params={'access_key':ACCES_KEY})
        cls.r = cls.req.json()

    def test_connection_API(self):
        self.assertEqual(self.req.status_code, 200)

    def test_good_acces_key(self):
        self.assertEqual(self.r['success'], True)

    @classmethod
    def tearDownClass(cls):
        pass


class TestCurrencyConverter(TestCase):
    @classmethod
    @requests_mock.Mocker()
    def setUpClass(cls, m):
        json_text = dumps(
            {
                'success': True, 'base': 'EUR', 'rates':
                {
                    'AED': 4, 'BTC': 0.01, 'CAD': 1.5,\
                    'CNY': 6.25, 'CZK': 25.0, 'EUR': 1, 'GBP': 0.8,\
                    'JPY': 125.5, 'PLN': 5, 'USD': 1.25
                }
            }
        )
        m.get(
            'http://data.fixer.io/api/latest',
            text=json_text
        )
        cls.app = CurrencyConverter('http://data.fixer.io/api/latest', {'acces_key': 123})

    def test_convert_base_int_code_code(self):
        self.assertEqual(
            len(self.app.convert(1, 'EUR', 'USD')['output'].keys()),
            1
        )
        self.assertEqual(
            self.app.convert(1, 'EUR', 'USD')['output']['USD'],
            1.25
        )

    def test_convert_base_int_code_sign(self):
        self.assertEqual(
            len(self.app.convert(1, 'EUR', '$')['output'].keys()),
            1
        )
        self.assertEqual(
            self.app.convert(1, 'EUR', '$')['output']['USD'],
            1.25
        )

    def test_convert_base_float_code_sign(self):
        self.assertEqual(
            len(self.app.convert(0.1, 'EUR', '$')['output'].keys()),
            1
        )
        self.assertEqual(
            self.app.convert(0.1, 'EUR', '$')['output']['USD'],
            0.12
        )

    def test_convert_base_float_sign_sign(self):
        self.assertEqual(
            len(self.app.convert(0.1, '€', '$')['output'].keys()),
            1
        )
        self.assertEqual(
            self.app.convert(0.1, '€', '$')['output']['USD'],
            0.12
        )
        self.assertEqual(
            self.app.convert(0.1, '€', '$')['input']['currency'],
            'EUR'
        )

    def test_convert_base_int_code(self):
        self.assertEqual(
            len(self.app.convert(1, 'EUR')['output'].keys()),
            10
        )
        self.assertEqual(
            self.app.convert(1, 'EUR', 'USD')['output']['USD'],
            1.25
        )

    def test_convert_base_int_sign(self):
        self.assertEqual(
            len(self.app.convert(1, '€')['output'].keys()),
            10
        )
        self.assertEqual(
            self.app.convert(1, 'EUR', 'USD')['output']['USD'],
            1.25
        )

    def test_convert_notbase_int_code_code(self):
        self.assertEqual(
            len(self.app.convert(1, 'PLN', 'CNY')['output'].keys()),
            1
        )
        self.assertEqual(
            self.app.convert(1, 'PLN', 'CNY')['output']['CNY'],
            1.25
        )

    def test_convert_notbase_int_code_sign(self):
        self.assertEqual(
            len(self.app.convert(1, 'PLN', '¥')['output'].keys()),
            1
        )
        self.assertEqual(
            self.app.convert(1, 'PLN', '¥')['output']['CNY'],
            1.25
        )

    def test_convert_notbase_float_code_sign(self):
        self.assertEqual(
            len(self.app.convert(0.1, 'PLN', '¥')['output'].keys()),
            1
        )
        self.assertEqual(
            self.app.convert(0.1, 'PLN', '¥')['output']['CNY'],
            0.12
        )

    def test_convert_notbase_float_sign_sign(self):
        self.assertEqual(
            len(self.app.convert(0.1, 'zł', '¥')['output'].keys()),
            1
        )
        self.assertEqual(
            self.app.convert(0.1, 'zł', '¥')['output']['CNY'],
            0.12
        )
        self.assertEqual(
            self.app.convert(0.1, 'zł', '¥')['input']['currency'],
            'PLN'
        )

    def test_convert_notbase_int_code(self):
        self.assertEqual(
            len(self.app.convert(1, 'PLN')['output'].keys()),
            10
        )
        self.assertEqual(
            self.app.convert(1, 'PLN')['output']['CNY'],
            1.25
        )

    def test_convert_notbase_int_sign(self):
        self.assertEqual(
            len(self.app.convert(1, 'ZŁ')['output'].keys()),
            10
        )
        self.assertEqual(
            self.app.convert(1, 'zł')['output']['CNY'],
            1.25
        )

    @classmethod
    def tearDownClass(cls):
        pass

class TestWebAPI(TestCase):
    @requests_mock.Mocker()
    def test_get_positive(self, m):
        json_text = dumps(
            {
                'success': True, 'base': 'EUR', 'rates':
                {
                    'AED': 4, 'BTC': 0.01, 'CAD': 1.5,\
                    'CNY': 6.25, 'CZK': 25.0, 'EUR': 1, 'GBP': 0.8,\
                    'JPY': 125.5, 'PLN': 5, 'USD': 1.25
                }
            }
        )
        m.get(
            'http://data.fixer.io/api/latest',
            text=json_text
        )
        response = app.test_client().get(
            '/currency_converter',
            data={
                'amount':10,
                'input_currency':'EUR',
                'output_currency':'PLN'
            }
        )
        self.assertEqual(response.status_code, 200)

    @requests_mock.Mocker()
    def test_get_401(self, m):
        json_text = dumps(
            {
                'success': False, 'base': 'EUR', 'rates':
                {
                    'AED': 4, 'BTC': 0.01, 'CAD': 1.5,\
                    'CNY': 6.25, 'CZK': 25.0, 'EUR': 1, 'GBP': 0.8,\
                    'JPY': 125.5, 'PLN': 5, 'USD': 1.25
                }
            }
        )
        m.get(
            'http://data.fixer.io/api/latest',
            text=json_text
        )
        response = app.test_client().get(
            '/currency_converter',
            data={
                'amount':10,
                'input_currency':'EUR',
                'output_currency':'PLN'
            }
        )
        self.assertEqual(response.status_code, 401)

    @requests_mock.Mocker()
    def test_get_410(self, m):
        m.get(
            'http://data.fixer.io/api/latest',
            status_code=503
        )
        response = app.test_client().get(
            '/currency_converter',
            data={
                'amount':10,
                'input_currency':'EUR',
                'output_currency':'PLN'
            }
        )
        self.assertEqual(response.status_code, 410)

    @requests_mock.Mocker()
    def test_get_BAD_REQUESTS(self, m):
        json_text = dumps(
            {
                'success': True, 'base': 'EUR', 'rates':
                {
                    'AED': 4, 'BTC': 0.01, 'CAD': 1.5,\
                    'CNY': 6.25, 'CZK': 25.0, 'EUR': 1, 'GBP': 0.8,\
                    'JPY': 125.5, 'PLN': 5, 'USD': 1.25
                }
            }
        )
        m.get(
            'http://data.fixer.io/api/latest',
            text=json_text
        )
        response = app.test_client().get(
            '/currency_converter',
            data={
                'amount':10,
                'input_currency':'blelble',
                'output_currency':'PLN'
            }
        )
        self.assertEqual(response.status_code, 400)


class TestCliApplication(TestCase):
    @requests_mock.Mocker()
    def test_positive_cli(self, m):
        json_text = dumps(
            {
                'success': True, 'base': 'EUR', 'rates':
                {
                    'AED': 4, 'BTC': 0.01, 'CAD': 1.5,\
                    'CNY': 6.25, 'CZK': 25.0, 'EUR': 1, 'GBP': 0.8,\
                    'JPY': 125.5, 'PLN': 5, 'USD': 1.25
                }
            }
        )
        m.get(
            'http://data.fixer.io/api/latest',
            text=json_text
        )
        runner = CliRunner()
        result = runner.invoke(cli_convert, ['--amount', 10, '--input_currency', 'EUR', '--output_currency', 'PLN'])
        self.assertEqual(
            result.output,
            '{\"input\": {\"amount\": 10.0, \"currency\": \"EUR\"}, \"output\": {\"PLN\": 50.0}}\n'
        )

    @requests_mock.Mocker()
    def test_negative_cli(self, m):
        json_text = dumps(
            {
                'success': True, 'base': 'EUR', 'rates':
                {
                    'AED': 4, 'BTC': 0.01, 'CAD': 1.5,\
                    'CNY': 6.25, 'CZK': 25.0, 'EUR': 1, 'GBP': 0.8,\
                    'JPY': 125.5, 'PLN': 5, 'USD': 1.25
                }
            }
        )
        m.get(
            'http://data.fixer.io/api/latest',
            text=json_text
        )
        runner = CliRunner()
        result = runner.invoke(cli_convert, ['--amount', 10, '--input_currency', 'blelbel', '--output_currency', 'PLN'])
        self.assertEqual(
            result.output,
            '{\"error_message\": \"Currency doesn\'t exist\"}\n'
        )

if __name__ == '__main__':
    main()