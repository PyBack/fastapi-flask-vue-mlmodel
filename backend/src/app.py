import os
import site
import traceback

from logging.config import dictConfig

from flask import Flask
from flask_cors import CORS
from flask_restx import Api

src_path = os.path.dirname(__file__)
pjt_home_path = os.path.join(src_path, os.pardir)
pjt_home_path = os.path.abspath(pjt_home_path)
site.addsitedir(pjt_home_path)

from views import controller as ctrl

# Flask 환경 변수
FLASK_ENV = 'development'
FLASK_RUN_PORT = 5500
FLASK_DEBUG = True

# Flask root logger config
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '%(asctime)s [%(levelname)s] {%(filename)s %(lineno)d} {%(funcName)s}: %(message)s',
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

ctrl.create_ml_model_namespace()
app.register_blueprint(ctrl.blueprint)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/')
def health_check():
    msg = 'Flask API Good!!'
    app.logger.info(msg)
    return msg


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=FLASK_RUN_PORT, debug=FLASK_DEBUG)
