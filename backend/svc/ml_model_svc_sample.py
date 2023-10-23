from flask import current_app
from flask_restx import Resource, Namespace
from flask_restx import reqparse

ml_model_ns_v2 = Namespace('ml_model', 'ML model service v2')


# @ml_model_ns_predict_v2.route('/sample')
class MLModelSample(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('ticker', type=str, help='Ticker')
    parser.add_argument('sector', type=str, help='sector choice: ', default='all',
                        choices=['all', 'tech', 'energy', 'financial']
                        )

    @ml_model_ns_v2.expect(parser)
    @ml_model_ns_v2.doc(responses={
        200: 'Success',
        400: 'Bad Request: 입력값 유효성 실패',
        404: 'Not Found',
        429: 'Too Many Requests',
        500: 'Internal Server Error:  REST-API 서버 자체 애러, ticker 이름 길이가 4를 초과 하면 애러 발생',
    })
    def get(self):
        """
        Ticker, Sector echo 기능
        """
        args = self.parser.parse_args()
        ticker = args['ticker']
        sector = args['sector']

        # print(ticker)
        current_app.logger.info("ticker: " + ticker)
        current_app.logger.info("sector: " + sector)

        # # error code test
        # if len(ticker) > 4:
        #     current_app.logger.warning("len(ticker) > 4")
        #     tmp = int(ticker)
        #     raise "len(ticker) > 4"

        return [ticker, sector], 200
