from django.shortcuts import render_to_response, redirect

from bindings import gsevol as Gse
from bindings.base import GseError


def request_params(request):
    return request.GET.get("gene"), request.GET.get("species")

def fill_gene_and_species(request):
    """Retrieve values of 'gene' and 'species' params from request.
    If neither is given, generate random example trees in their place.
    """
    gene, species = request_params(request)
    if gene is None and species is None:
        try:
            gene, species = Gse.random_trees()
        except Exception as e:
            raise RuntimeError("Problem processing Gsevol output", e)
    return gene, species


def form_data(request, unrooted=False):
    gene, species = fill_gene_and_species(request)
    data = {
        "default_gene": gene or '',
        "default_species": species or '',
        "form_url": "/rooted/",
        "result_component": "RootedApp",
        "show_results": False,
        "form_template": "rooted_form.html"
    }
    if unrooted:
        data.update({
            "form_url": "/unrooted/",
            "result_component": "UnrootedApp",
            "form_template": "unrooted_form.html"
        })
    return data


def index(request, unrooted=False):
    data = form_data(request, unrooted)
    if any(request_params(request)):
        data["show_results"] = True
    return render_to_response("index.html", data)


def unrooted_index(request):
    return index(request, unrooted=True)

def scenario_index(request):
    scenario = request.GET.get("scenario", '')
    show_results = bool(scenario)
    gene, species = request_params(request)
    if not scenario and gene and species:
        try:
            scenario = Gse.optscen(gene, species)
        except GseError:
            pass
    template_data = {
        "default_scenario": scenario or '',
        "default_species": species or '',
        "form_url": "/scenario/",
        "result_component": "ScenarioApp",
        "show_results": show_results,
        "form_template": "scenario_form.html",
    }
    return render_to_response("index.html", template_data)

def diagram(request):
    gene, species = request_params(request)
    if gene and species:
        result = Gse.draw_diagram(gene, species)
    else:
        return redirect('front.views.index')
    return render_to_response("diagram.html", {"picture": result})


