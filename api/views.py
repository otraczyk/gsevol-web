# -*- coding: utf-8 -*
import json

from api.view_utils import JsonResponse, pass_errors_to_response, deploy_tasks
from bindings import gsevol as Gse
from bindings import urec as Urec

from bindings import tasks


@pass_errors_to_response
def draw(request):
    """Provide basic data for one or two rooted trees.

    For single tree: draw tree.

    For both gene and species trees:
        * 3 pics: gene and species trees and their mapping
        * optimal evoultionary scenario and corresponding embedding pic
        * list of all possible scenarios

    All pictures are returned as svg source.
    """
    delegables = [
        tasks.DrawGene,
        tasks.DrawSpecies,
        tasks.DrawMapping,
        tasks.OptScen,
        tasks.AllScenarios,
    ]
    deploy_tasks(delegables, request)
    return JsonResponse()


@pass_errors_to_response
def draw_single(request):
    tree = json.loads(request.body)
    picture = Gse.draw_single_tree(tree)
    return JsonResponse(picture)

@pass_errors_to_response
def draw_embedding(request):
    input_trees = json.loads(request.body)
    scenario, species = input_trees.get("scenario"), input_trees.get("species")
    if scenario and species:
        result = Gse.draw_embedding(species, scenario)
        return JsonResponse(result)
    else:
        msg = "'scenario' and 'species' are required"
        return JsonResponse(msg, status=400)

@pass_errors_to_response
def draw_diagram(request):
    deploy_tasks((tasks.DrawDiagram,), request)
    return JsonResponse()

@pass_errors_to_response
def draw_unrooted(request):
    delegables = [tasks.DrawUnrooted, tasks.OptRootings, tasks.DrawSpecies]
    deploy_tasks(delegables, request)
    return JsonResponse()

@pass_errors_to_response
def scenario(request):
    delegables = [tasks.Scenario, tasks.DrawSpecies]
    deploy_tasks(delegables, request)
    return JsonResponse()


