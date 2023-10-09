import requests

from flask import current_app
from flask_restx import Resource, Namespace
from flask_restx import reqparse


ml_model_ns_v2 = Namespace('ml_model', 'ML model service v2')


class MLModelEPS(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('ticker', type=str, help='Ticker')

    @ml_model_ns_v2.expect(parser)
    @ml_model_ns_v2.doc(responses={
        200: 'Success (Accept)',
        400: 'Bad Request: 입력값 유효성 실패',
        404: 'Not Found',
        429: 'Too Many Requests',
        500: 'Internal Server Error:  REST-API 서버 자체 애러, /////',
    })
    def get(self):
        """
        EPS 예측 모델 실행
        """
        args = self.parser.parse_args()
        ticker = args['ticker']

        current_app.logger.info("ticker: " + ticker)

        # step.1: validation check

        # step.2: call ML model prediction pod
        # response = requests.get('http://localhost:5505/eps-prediction')

        # step.3: recv response

        return ticker, 200
