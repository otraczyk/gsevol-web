# -*- coding: utf-8 -*
import json

from api.view_utils import JsonResponse, pass_errors_to_response
from bindings import gsevol as Gse
from bindings import urec as Urec
from bindings.tasks import launch_async

import api.operations as O


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
        launch_async(O.draw_gene_species_mapping, (gene, species), request)

        launch_async(O.all_scenarios, (gene, species), request)

        launch_async(O.opt_scen, (gene, species), request)
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
    gene, species = req_params["gene"], req_params["species"]
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
