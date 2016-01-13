from django.shortcuts import render_to_response

from api import bindings as Gse


def index(request):
    defaults = {}
    try:
        # Provide random trees as defaults for input form.
        gene, species = Gse.random_trees().split("\n")[:2]
        defaults = {"default_gene": gene.strip(), "default_species": species.strip()}
    except Exception as e:
        raise RuntimeError("Problem processing Gsevol output", e)
    return render_to_response("index.html", defaults)


def results(request):
    """Render results page
    """
    form_defaults = {
        "default_gene": request.GET.get("gene"),
        "default_species": request.GET.get("species")
    }
    return render_to_response("results.html", form_defaults)
