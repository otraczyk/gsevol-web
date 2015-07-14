from django.shortcuts import render_to_response

from api import bindings as Gse

def demo(request):
    random_tree_svg = Gse.draw_randbin_s()
    return render_to_response('base.html', {'content': random_tree_svg})

def index(request):
    defaults = {}
    try:
        # Provide random trees as defaults for input form.
        gene, species = Gse.gen_randbin_f().split('\n')[:2]
        defaults = {'default_gene': gene, 'default_species': species}
    except Exception as e:
        raise RuntimeError("Problem processing Gsevol output", e)
    return render_to_response('index.html', defaults)
