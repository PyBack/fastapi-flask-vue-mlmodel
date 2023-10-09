from flask import Flask, Response
from messageannouncer import MessageAnnouncer

# Flask 환경 변수
FLASK_ENV = 'development'
FLASK_RUN_PORT = 5500
FLASK_DEBUG = True

app = Flask(__name__)

announcer = MessageAnnouncer()


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
    print(msg)
    return msg


@app.route('/ping')
def ping():
    msg = format_sse(data='pong', event='optimizer state')
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
