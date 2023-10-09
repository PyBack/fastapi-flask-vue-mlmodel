import os
import site
import traceback

from logging.config import dictConfig

from flask import Flask, Response
from flask import Blueprint
from flask import current_app
from flask_cors import CORS
from flask_restx import Api, Resource

from messageannouncer import MessageAnnouncer

# Flask 환경 변수
FLASK_ENV = 'development'
FLASK_RUN_PORT = 5500
FLASK_DEBUG = True

# Flask-RESTX를 사용하기 위한 설정
app = Flask(__name__)
# blueprint = Blueprint('api_2', __name__, url_prefix='/api/v2')
# api = Api(blueprint, version='0.2',
#           title='Flask API',
#           description='Flask API Structure Test',
#           )
#
# app.register_blueprint(blueprint)

announcer = MessageAnnouncer()

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

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


def format_sse(data: str, event=None) -> str:
    """
    The event parameter is optional, it allows defining topics
    to which clients can subscribe to.
    :param data:
    :param event:
    :return: msg
    """
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg


@app.route('/')
def health_check():
    msg = 'Flask API Good!!'
    app.logger.info(msg)
    return msg


@app.route('/ping')
def ping():
    msg = format_sse(data='pong', event='optimizer state')
    app.logger.info('\n' + msg)
    announcer.announce(msg=msg)
    return {}, 200


@app.route('/listen', methods=['GET'])
def listen():

    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg

    return Response(stream(), mimetype='text/event-stream')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=FLASK_RUN_PORT, debug=FLASK_DEBUG)
