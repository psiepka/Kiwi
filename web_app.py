"""Simple web application, which convert current currency."""
from flask import Flask
from flask_restful import Resource, Api, reqparse
from dotenv import load_dotenv
from os import getenv
from main import CurrencyConverter


load_dotenv()
ACCES_KEY = getenv('ACCES_KEY')
print(ACCES_KEY)
app = Flask(__name__)
api = Api(app)

class ConvertApp(Resource):
    '''Convert class serializer, which convert currency.
    Arguments:
        amount [float/integer] - amount which we want to convert - float
        input_currency [string] - input currency - 3 letters name or currency symbol
        output_currency [string] - requested/output currency - 3 letters name or currency symbol
    Returns:
        GET /currency_converter?amount=<amount:float/int>&input_currency=<currency:string>&output_currency=<currency:string> HTTP/1.1
            - return json currency convcert data
    '''

    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument(
                'amount', type=float, required=True,
                help='[float/integer] -- Amount which we want to convert [required]'
            )
            parser.add_argument(
                'input_currency', required=True,
                help='string] Input currency - 3 letters name or currency symbol [required]'
            )
            parser.add_argument(
                'output_currency',
                help='Requested/output currency - [string] 3 letters name or currency symbol.'
            )
            args = parser.parse_args()
            # return {'amount':args['amount'], 'input_currency':args['input_currency'], 'output_currency':args['output_currency']}
            app = CurrencyConverter(
                api_url='http://data.fixer.io/api/latest', api_params={'access_key': ACCES_KEY}
            )
            return app.convert(amount=args['amount'], input_currency=args['input_currency'], output_currency=args['output_currency'])
        except AttributeError as e:
            return e.args[0]

api.add_resource(ConvertApp, '/currency_converter', endpoint='convert_app')

if __name__ == '__main__':
    app.run(debug=True) # change after all on False
