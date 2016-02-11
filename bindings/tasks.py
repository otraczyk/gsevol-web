from settings import app
from api.view_utils import broadcast_message
from bindings.base import GseError
from bindings import gsevol as Gse
from bindings import urec as Urec

@app.task
def add(x, y):
    """Test task.
    """
    return x + y

# TODO: Find a way to get rid of copy-paste.
# with a decorator all tasks are named "wrapper" and only the last one works.
def broadcast_results(op_func):
    def wrapper(channel, *args, **kwargs):
        try:
            results = op_func(*args)
            broadcast_message(results, channel)
        except GseError as exc:
            broadcast_message({"error": str(exc)}, channel)
    return wrapper


@app.task
def draw_gene_species(channel, gene, species):
    try:
        gtree, stree = Gse.draw_trees(gene, species)
        results = {"gene": gtree, "species": stree}
        broadcast_message(results, channel)
    except GseError as exc:
        broadcast_message({"error": str(exc)}, channel)

@app.task
def draw_mapping(channel, gene, species):
    try:
        mapping = Gse.draw_mapping(gene, species)
        results = {"mapping": mapping}
        broadcast_message(results, channel)
    except GseError as exc:
        broadcast_message({"error": str(exc)}, channel)

@app.task
def all_scenarios(channel, gene, species):
    try:
        results = {"scenarios": Gse.scenarios(gene, species)}
        broadcast_message(results, channel)
    except GseError as exc:
        broadcast_message({"error": str(exc)}, channel)

@app.task
def opt_scen(channel, gene, species):
    try:
        optimal = Gse.optscen(gene, species)
        results = {
            "optscen": {
                'scen': optimal,
                'pic': Gse.draw_embedding(species, optimal)
                }
            }
        broadcast_message(results, channel)
    except GseError as exc:
        broadcast_message({"error": str(exc)}, channel)
