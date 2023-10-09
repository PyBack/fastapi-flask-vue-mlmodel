import os
import site
import traceback

import requests

from logging.config import dictConfig
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, request
from flask import current_app
from flask_cors import CORS
from flask_restx import Api, Resource

# Flask 환경 변수
FLASK_ENV = 'development'
FLASK_RUN_PORT = 5500
FLASK_DEBUG = True

# Flask root logger config
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '%(asctime)s [%(levelname)s] %(filename)s %(lineno)d: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://sys.stdout',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

# Flask-RESTX를 사용하기 위한 설정
app = Flask(__name__)
api = Api(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# ThreadPoolExecutor를 사용하여 비동기 작업을 수행합니다.
executor = ThreadPoolExecutor(max_workers=10)


# `/predict` API를 구현합니다.
@api.get("/predict")
class Predict(Resource):
    def get(self):
        # 요청 데이터를 로딩
        data = request.get_json()

        # # 요청을 비동기 방식으로 처리합니다. (from BARD) ???
        # future = executor.submit(predict, data)
        #
        # # 응답을 로딩 중 상태로 설정합니다.
        # response = {"status": "loading"}
        #
        # # 요청이 완료될 때까지 대기합니다.
        # try:
        #     response["result"] = future.result()
        # except Exception as e:
        #     err_msg = traceback.format_exc()
        #     current_app.logger.error(err_msg)
        #     response["error"] = str(e)

        return redirect(url_for('.hidden_async'), code=307)


@api.route('/hidden-async', methods=['GET'])
async def hidden_async(data):
    result = await predict(data)
    return result


# `predict` 함수를 사용하여 외부 REST API를 호출합니다.
def predict(data):
    # 외부 REST API를 호출합니다.
    response = requests.get("https://example.com/predict", json=data)

    # 응답을 JSON으로 파싱합니다.
    result = response.json()

    # 응답을 반환합니다.
    return result




# 서버를 실행합니다.
if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=os.environ.get('FLASK_RUN_PORT'), debug=os.environ.get('FLASK_DEBUG'))
    app.run(host='0.0.0.0', port=FLASK_RUN_PORT, debug=FLASK_DEBUG)
