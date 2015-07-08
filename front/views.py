from django.shortcuts import render_to_response

from api import bindings as Gse

def demo(request):
    random_tree_svg = Gse.draw_randbin_s()
    return render_to_response('base.html', {'content': random_tree_svg})
