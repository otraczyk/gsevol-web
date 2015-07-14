# -*- coding: utf-8 -*
import json
from functools import partial
from django.http import HttpResponse

from api import bindings as Gse

JsonResponse = lambda data: HttpResponse(json.dumps(data),
                                                 # status=status,
                                                 content_type="application/json")

def draw(request):
    svg = Gse.draw_randbin_s()
    return JsonResponse({'svg': svg})
