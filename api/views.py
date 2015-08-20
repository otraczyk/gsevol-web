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
    results = {}
    try:
        if input_trees["gene"] and input_trees["species"]:
            # processing double input
            svgs = Gse.draw_trees(input_trees["gene"], input_trees["species"])
            results = {"gene": svgs[0], "species": svgs[1], "mapping": svgs[2]}
            scenarios = Gse.scenarios(input_trees["gene"], input_trees["species"])
            results["scenarios"] = scenarios
        else:
            for tree_type in ["gene", "species"]:
                if input_trees[tree_type]:
                    svg = Gse.draw_single_tree(input_trees[tree_type])
                    results[tree_type] = svg
        return JsonResponse(results)
    except Gse.GseError as exc:
        # error = re.search(r'Exception\("([^"]*)', str(exc)).group(1)
        return JsonResponse(str(exc), status=500)
    except Exception as exc:
        if settings.DEBUG:
            error = str(exc)
        else:
            error = "Server error"
        return JsonResponse(error, status=500)

def draw_embedding(request):
    # TODO: REFACTOR! Late evening code.
    input_trees = json.loads(request.body)
    input_trees = {d["name"]: d["value"] for d in input_trees}
    if input_trees["scenario"] and input_trees["species"]:
        try:
            result = Gse.draw_embedding(input_trees["species"], input_trees["scenario"])
            return JsonResponse(result)
        except Gse.GseError as exc:
            # error = re.search(r'Exception\("([^"]*)', str(exc)).group(1)
            return JsonResponse(str(exc), status=500)
        except Exception as exc:
            if settings.DEBUG:
                error = str(exc)
            else:
                error = "Server error"
                return JsonResponse(error, status=500)
    error = "Server error"
    return JsonResponse(error, status=500)

