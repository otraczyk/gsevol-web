# -*- coding: utf-8 -*
import re
import json
import urllib

from ws4redis.redis_store import RedisMessage
from ws4redis.publisher import RedisPublisher

from django.http import HttpResponse
from django.conf import settings

from bindings.base import GseError

JsonResponse = lambda data='', status=200: HttpResponse(
    json.dumps(data),
    status=status,
    content_type="application/json"
)

def error_message(exception):
    error = re.search(r'(Exception\("([^"]*)|([A-Z]+\w*Error: ([^"\["]*)))', str(exception))
    if error:
        error = error.group(1)
    elif settings.DEBUG:
        error = str(exception)
    else:
        error = "Server error"
    return error

def pass_errors_to_response(view_func):
    def wrapper(request):
        try:
            return view_func(request)
        except GseError as exc:
            error = error_message(exc)
            return JsonResponse(error, status=500)
        except Exception as exc:
            error = error_message(exc)
            return JsonResponse(error, status=500)

    return wrapper

def broadcast_message(text, channel):
    """Send broadcast message to a websocket.
    """
    msg = RedisMessage(json.dumps(text))
    RedisPublisher(facility=channel, broadcast=True).publish_message(msg)


class ProcessedRequest(object):

    def __init__(self, http_request):
        self.socket = self.websocket_channel(http_request)
        req_body = json.loads(http_request.body)
        self.params = {}
        for param, value in req_body.items():
            self.params[param] = value

    def check_required_params(self, params):
        for param in params:
            assert self.params.get(param), "Required params: %s" % (params,)

    def websocket_channel(self, request):
        """Get redis channel id for websocket corresponding to given request.

        Currently it's simply query string from refering view.
        """
        channel = request.META["HTTP_REFERER"].split('?')[1]
        channel = urllib.unquote(channel).decode('utf8')
        return channel

def deploy_tasks(task_list, request):
    proc_req = ProcessedRequest(request)
    for task_class in task_list:
        task = task_class()
        task.req = proc_req
        task.deploy()
