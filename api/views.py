# -*- coding: utf-8 -*
import re
import json
from django.http import HttpResponse
from django.conf import settings

from api import bindings as Gse

JsonResponse = lambda data, status=200: HttpResponse(
    json.dumps(data),
    status=status,
    content_type="application/json"
)

def draw(request):
    input_trees = json.loads(request.body)
    # Flattening list of dicts
    input_trees = {d["name"]: d["value"] for d in input_trees}
    try:
        svg = Gse.draw_trees(input_trees["gene"], input_trees["species"])
        return JsonResponse({'svg': svg})
    except Gse.GseError as exc:
        error = re.search(r'Exception\("([^"]*)', str(exc)).group(1)
        return JsonResponse(error, status=500)
    except Exception as exc:
        if settings.DEBUG:
            error = str(exc)
        else:
            error = "Server error"
        return JsonResponse(error, status=500)
