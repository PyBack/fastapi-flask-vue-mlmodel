from flask import current_app, request, Response
from flask_restx import Resource, Namespace, fields
from flask_restx import reqparse

from svc.messageannouncer import MessageAnnouncer

ml_model_ns_v2 = Namespace('ml_model', 'ML model service v2')


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


# model = ml_model_ns_predict_v2.model('new article',
#                                      strict=True,
#                                      model={'writer': fields.String(title='글 작성자', default='writer', required=True),
#                                     'password': fields.String(title='비밀번호', default='password', required=True),
#                                     'category': fields.String(title='글 카테고리', default='잡담', required=True),
#                                     'title': fields.String(title='글 제목', default='title', required=True),
#                                     'description': fields.String(title='글 본문', default='description', required=True),
#                                     }
#                                      )
class DictItem(fields.Raw):
    def output(self, key, obj, *args, **kwargs):
        try:
            dct = getattr(obj, self.attribute)
        except AttributeError:
            return {}
        return dct or {}


resource_fields = ml_model_ns_v2.model(name='ml model predict input',
                                       model={'ticker': fields.String(required=True, title='ticker'),
                                              'data': fields.String(required=True, title='data')}
                                       )


class MLModelEPSPredictRequest(Resource):
    announcer = MessageAnnouncer()

    @ml_model_ns_v2.doc(responses={
        200: 'Success',
        400: 'Bad Request: 입력값 유효성 실패',
        404: 'Not Found',
        429: 'Too Many Requests',
        500: 'Internal Server Error:  REST-API 서버 자체 애러, /////',
    })
    # @ml_model_ns_v2.expect(resource_fields, validate=True)
    def post(self):
        """
        EPS 예측 모델 결과 등록 (ML model Pod 대응)
        """
        if not request.is_json:
            current_app.logger.info('body is not json')
            return {}, 400

        json_data = request.get_json(force=True)
        current_app.logger.info("json_data \n" + str(json_data))

        # announcer 에 append 되는 메시지는 바로 FrontEnd 에 전달됨

        msg = format_sse(data=json_data['data'], event='ml_model/eps')
        current_app.logger.info('format sse\n' + msg)
        self.announcer.announce(msg=msg)
        return {}, 200

    @ml_model_ns_v2.doc(responses={
        200: 'Success',
        400: 'Bad Request: 입력값 유효성 실패',
        404: 'Not Found',
        429: 'Too Many Requests',
        500: 'Internal Server Error:  REST-API 서버 자체 애러, /////',
    })
    def get(self):
        """
        EPS 예측 모델 결과 Notification Listen (FrontEnd 대응)
        """
        def stream():
            messages = self.announcer.listen()  # returns a queue.Queue
            while True:
                msg = messages.get()  # blocks until a new message arrives
                yield msg

        return Response(stream(), mimetype='text/event-stream')
