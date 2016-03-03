# -*- coding: utf-8 -*
from celery import Task
from settings import app
from django.conf import settings

from api.view_utils import broadcast_message, ProcessedRequest, error_message
from api.styling import make_options
from bindings.base import GseError
from bindings import gsevol as Gse
from bindings import urec as Urec


class GseTask(Task):
    """
    Supports two ways of launching tasks:

    ** Async: delegate task to celery.
    ** Traditional: run task function directly
    Results are send via websocket.
    """
    required_params = []
    variable_translations = {}

    def __init__(self, request=None):
        Task.__init__(self)
        if request:
            self.req = ProcessedRequest(request)

    def deploy(self):
        # Tricky: we need to pass the arguments to self.delay (and as a result
        # self.core), even if it should be able to access it from self.
        # Code from delay()/run() is being run inside celery task and has no access
        # to attributes calculated at runtime.
        try:
            self.prepare()
            if settings.DELEGATE_TASKS:
                self.delay(self.params, self.req.socket)
            else:
                result = self.core(self.params)
                self.send_result(result)
        except (GseError, AssertionError) as exc:
            self.send_error(error_message(exc))

    def send_result(self, data):
        broadcast_message(data, self.req.socket)

    def send_error(self, message):
        self.send_result({"error": message})

    def run(self, params, socket):
        result = self.core(params)
        broadcast_message(result, socket)

    def prepare(self):
        self.req.check_required_params(self.required_params)
        self.params = self.other_params
        for param in self.required_params:
            self.params[param] = self.req.params[param]
        for task_name, binding_name in self.variable_translations.items():
            self.params[binding_name] = self.params.pop(task_name)
        if 'options' in self.params:
            conf = self.req.params.get("config", {}).get(self.kind, {})
            self.params["options"] = make_options(self.kind, conf)

    def core(self, params):
        raise NotImplemented


class DrawGene(GseTask):
    kind = "gene"
    required_params = ("gene",)
    other_params = {"options": ""}
    variable_translations = {"gene": "tree"}
    def core(self, params):
        gtree = Gse.draw_single_tree(**params)
        return {"gene": gtree}

class DrawSpecies(GseTask):
    kind = "species"
    required_params = ("species",)
    other_params = {"options": ""}
    variable_translations = {"species": "tree"}
    def core(self, params):
        stree = Gse.draw_single_tree(**params)
        return {"species": stree}

class DrawMapping(GseTask):
    kind = "mapping"
    required_params = ("gene", "species")
    other_params = {"options": ""}
    def core(self, params):
        mapping = Gse.draw_mapping(**params)
        return {"mapping": mapping}

class AllScenarios(GseTask):
    kind = "scenarios"
    required_params = ("gene", "species")
    other_params = {"options": ""}
    def core(self, params):
        return {"scenarios": Gse.scenarios(**params)}

class Scenario(GseTask):
    kind = "scenario"
    required_params = ("species", "scen")
    other_params = {"options": "", "name": "scenario"}
    def core(self, params):
        scen = params["scen"]
        d, l = Gse.scenario_cost(scen)
        return {
            params["name"]: {
            'scen': scen,
            'pic' : Gse.draw_embedding(params["species"], scen, params["options"]),
            'cost': {'dups': d, 'losses': l}
            }
        }

class OptScen(GseTask):
    kind = "optscen"
    required_params = ("gene", "species")
    other_params = {"options": ""}
    def core(self, params):
        optimal = Gse.optscen(**params)
        scenario_params = {
            "scen": optimal,
            "species": params["species"],
            "name": "optscen",
            "options": params["options"]
        }
        return Scenario().core(scenario_params)

class DrawUnrooted(GseTask):
    kind = "unrooted"
    required_params = ("gene", "species")
    other_params = {"options": "", "cost": "DL"}
    def core(self, params):
        utree = Urec.draw_unrooted(**params)
        return {self.kind: utree}
