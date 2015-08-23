from django.shortcuts import render_to_response

from api import bindings as Gse


def index(request):
    defaults = {}
    try:
        # Provide random trees as defaults for input form.
        gene, species = Gse.random_trees().split('\n')[:2]
        defaults = {'default_gene': gene, 'default_species': species}
    except Exception as e:
        raise RuntimeError("Problem processing Gsevol output", e)
    return render_to_response('index.html', defaults)
