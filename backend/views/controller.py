from flask import current_app
from flask import Blueprint
from flask_restx import Api, Namespace
# from flask_request_validator import *
# from flask_request_validator.exceptions import InvalidRequestError
# from flask_request_validator.error_formatter import demo_error_formatter

from svc.ml_model_svc_eps import MLModelEPS
from svc.ml_model_svc_eps_predict_result import MLModelEPSPredictResult
from svc.ml_model_svc_sample import MLModelSample


blueprint = Blueprint('api_2', __name__, url_prefix='/api/v2')
api = Api(blueprint, title='Flask API v0.2', version='0.2', description='Flask API v0.2')

ml_model_ns_v2 = Namespace('ml_model', 'ML model service v2')


@api.errorhandler
def default_error_handler(error):
    """
    Default error handler of api_2
    """
    # msg = traceback.format_exc()
    # Debug_mode: Ture 인 경우에 error 항목에 interactive debugger 모드가 생성됨
    # 따라서 Debug_mode: False 인 경우만 500 의 별도 메시지 출력 필요
    status_code = getattr(error, 'code', 500)

    if current_app.debug is False & status_code == 500:
        msg = '관리자에게 문의'
    else:
        msg = str(error)

    return {'message': msg}, status_code


def create_ml_model_namespace():
    api.add_namespace(ml_model_ns_v2)

    ml_model_ns_v2.add_resource(MLModelEPS, '/eps-predict-request')
    ml_model_ns_v2.add_resource(MLModelEPSPredictResult, '/eps-predict-result')
    ml_model_ns_v2.add_resource(MLModelSample, '/sample')
