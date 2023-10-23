import requests

from flask import current_app, request
from flask_restx import Resource, Namespace
from flask_restx import fields


ml_model_ns_v2 = Namespace('ml_model', 'ML model service v2')

resource_fields = ml_model_ns_v2.model(name='ml model predict input (user)',
                                       model={'ticker': fields.String(required=True, title='ticker')}
                                       )


class MLModelEPS(Resource):
    # @ml_model_ns_v2.expect(resource_fields)
    @ml_model_ns_v2.doc(responses={
        200: 'Success (Accept)',
        400: 'Bad Request: 입력값 유효성 실패',
        404: 'Not Found',
        429: 'Too Many Requests',
        500: 'Internal Server Error:  REST-API 서버 자체 애러, /////',
    })
    def post(self):
        """
        EPS 예측 모델 실행
        """
        json_data = request.get_json(force=True)
        ticker = json_data['ticker']

        current_app.logger.info("ticker: " + ticker)

        # step.1: validation check

        # step.2: call ML model prediction pod
        # response = requests.get('http://localhost:5505/eps-prediction')

        # step.3: recv response

        return ticker, 200
