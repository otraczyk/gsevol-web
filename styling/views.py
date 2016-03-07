import json

from api.view_utils import JsonResponse, pass_errors_to_response
from styling.utils import rendering_task, get_available_options

@pass_errors_to_response
def options(request):
    params = json.loads(request.body)
    kind = params.get("kind")
    available_opts = get_available_options(kind)
    opt_list = [opt.serialize() for opt in available_opts]
    return JsonResponse(opt_list)

@pass_errors_to_response
def restyle(request):
    params = json.loads(request.body)
    kind = params.get("kind")
    task_class = rendering_task(kind)
    task = task_class(request).deploy()
    return JsonResponse()
