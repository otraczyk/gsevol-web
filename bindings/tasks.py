from celery import Task
from settings import app
from django.conf import settings

from api.view_utils import broadcast_message
from bindings.base import GseError
from bindings import gsevol as Gse
from bindings import urec as Urec


class GseTask(Task):
    """
    Supports two ways of launching tasks and communicating results:

    ** Async: delegate task to celery and send results via websocket.
    ** Traditional: run task directly, send results in http response.
    """
    def deploy(self, socket_channel, params):
        if settings.DELEGATE_TASKS:
            self.delay(socket_channel, *params)
            return {}  # for type consistency when falling back to rest.
        else:
            return self.core(*params)

    def run(self, socket_channel, *args, **kwargs):
        try:
            results = self.core(*args, **kwargs)
            broadcast_message(results, socket_channel)
        except GseError as exc:
            broadcast_message({"error": str(exc)}, socket_channel)

    def core(self, *args, **kwargs):
        raise NotImplemented


class DrawGene(GseTask):
    def core(self, gene, options=''):
        gtree = Gse.draw_single_tree(gene, options)
        return {"gene": gtree}

class DrawSpecies(GseTask):
    def core(self, species, options=''):
        stree = Gse.draw_single_tree(species)
        return {"species": stree}

class DrawMapping(GseTask):
    def core(self, gene, species):
        mapping = Gse.draw_mapping(gene, species)
        return {"mapping": mapping}

class AllScenarios(GseTask):
    def core(self, gene, species):
        return {"scenarios": Gse.scenarios(gene, species)}

class Scenario(GseTask):
    def core(self, scen, species, name="scenario"):
        d, l = Gse.scenario_cost(scen)
        return {name: {'scen': scen,
                       'pic' : Gse.draw_embedding(species, scen),
                       'cost': {'dups': d, 'losses': l}
                    }
                }

class OptScen(GseTask):
    def core(self, gene, species):
        optimal = Gse.optscen(gene, species)
        return Scenario().core(optimal, species, "optscen")
