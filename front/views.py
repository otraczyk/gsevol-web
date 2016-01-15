from django.shortcuts import render_to_response, redirect

from bindings import gsevol as Gse


def index(request):
    defaults = {}
    try:
        # Provide random trees as defaults for input form.
        gene, species = Gse.random_trees()
        defaults = {"default_gene": gene, "default_species": species}
    except Exception as e:
        raise RuntimeError("Problem processing Gsevol output", e)
    return render_to_response("index.html", defaults)


def results(request):
    form_defaults = {
        "default_gene": request.GET.get("gene"),
        "default_species": request.GET.get("species")
    }
    return render_to_response("results.html", form_defaults)


def diagram(request):
    gene, species = request.GET.get("gene"), request.GET.get("species")
    if gene and species:
        result = Gse.draw_diagram(gene, species)
    else:
        return redirect('front.views.index')
    return render_to_response("diagram.html", {"picture": result})
