# -*- coding: utf-8 -*
import json

from api.view_utils import JsonResponse, pass_errors_to_response, websocket_channel
from api.styling import rendering_task, make_options
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
    results = {}
    input_trees = json.loads(request.body)
    gene, species = input_trees.get("gene"), input_trees.get("species")

    if gene and species:
        ws = websocket_channel(request)
        delegables = [
            (tasks.DrawGene(), [gene]),
            (tasks.DrawSpecies(), [species]),
            (tasks.DrawMapping(), (gene, species)),
            (tasks.OptScen(), (gene, species)),
            (tasks.AllScenarios(), (gene, species))
        ]
        for task, params in delegables:
            results.update(task.deploy(ws, params))
    else:
        for tree_type in ["gene", "species"]:
            if input_trees.get(tree_type):
                svg = Gse.draw_single_tree(input_trees[tree_type])
                results[tree_type] = svg
    return JsonResponse(results)


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
    input_trees = json.loads(request.body)
    gene, species = input_trees["gene"], input_trees["species"]
    if gene and species:
        result = Gse.draw_diagram(gene, species)
        return JsonResponse(result)
    else:
        msg = "'gene' and 'species' are required"
        return JsonResponse(msg, status=400)

@pass_errors_to_response
def draw_unrooted(request):
    req_params = json.loads(request.body)
    gene, species = req_params.get("gene"), req_params.get("species")
    cost = req_params.get("cost") or "DL"
    if gene and species:
        picture = Urec.draw_unrooted(gene, species, cost)
        rootings = Urec.optimal_rootings(gene, species, cost)
        species = Gse.draw_single_tree(species)
        return JsonResponse({
            "unrooted": picture,
            "rootings": rootings,
            "species": species
        })
    else:
        msg = "'gene' and 'species' are required"
        return JsonResponse(msg, status=400)

@pass_errors_to_response
def scenario(request):
    input_trees = json.loads(request.body)
    scenario, species = input_trees.get("scenario"), input_trees.get("species")
    if scenario and species:
        results = {}
        results.update(tasks.Scenario().core(scenario, species))
        results["species"] = Gse.draw_single_tree(species)
        return JsonResponse(results)
    else:
        msg = "'scenario' and 'species' are required"
        return JsonResponse(msg, status=400)

@pass_errors_to_response
def options(request):
    available_opts = [{
        "name": "scale",
        "label": "Scale",
        "default": 1,
        "input": "number",
    },{
        "name": "resolution",
        "label": "Resolution",
        "default": 1,
        "input": "number"
    }
    ]
    return JsonResponse(available_opts)

@pass_errors_to_response
def restyle(request):
    # params = json.loads(request.body)
    # kind, config = params.get("kind"), params.get("config")
    redraw_gene(request)
    return JsonResponse("OK")

def redraw_gene(request):
    # TODO: some refactor, sonmething's redundant here
    params = json.loads(request.body)
    gene, config = params.get("gene"), params.get("config", {})
    options_string = make_options("gene", config)
    ws = websocket_channel(request)
    task = tasks.DrawGene()
    task.deploy(ws, [gene, options_string])
