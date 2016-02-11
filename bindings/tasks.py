from settings import app
from api.view_utils import broadcast_message
from bindings.base import GseError

@app.task
def add(x, y):
    """Test task.
    """
    return x + y

@app.task
def launch_async(func, args, request):
    """Celery task that launches a function with args then sends results
    via websocket.
    """
    # TODO: convert to decorator?
    try:
        results = func(*args)
        broadcast_message(results, request)
    except GseError as exc:
        broadcast_message(str(ext), request)
