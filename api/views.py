# -*- coding: utf-8 -*
import json
from functools import partial
from django.http import HttpResponse

from api import bindings as Gse

JsonResponse = lambda data: HttpResponse(json.dumps(data),
                                                 # status=status,
                                                 content_type="application/json")

def draw(request):
    input_trees = json.loads(request.body)
    # Flattening list of dicts
    input_trees = {d["name"]: d["value"] for d in input_trees}

    svg = Gse.draw_genes(input_trees["gene"])
    return JsonResponse({'svg': svg})
