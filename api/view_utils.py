# -*- coding: utf-8 -*
import re
import json
from django.http import HttpResponse
from django.conf import settings

from api.bindings import GseError

JsonResponse = lambda data, status=200: HttpResponse(
    json.dumps(data),
    status=status,
    content_type="application/json"
)

def pass_errors_to_response(view_func):
    def wrapper(request):
        try:
            return view_func(request)
        except GseError as exc:
            # error = re.search(r'Exception\("([^"]*)', str(exc)).group(1)
            return JsonResponse(str(exc), status=500)
        except Exception as exc:
            if settings.DEBUG:
                error = str(exc)
            else:
                error = "Server error"
            return JsonResponse(error, status=500)

    return wrapper
