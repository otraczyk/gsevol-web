# -*- coding: utf-8 -*
from celery import Task
from settings import app
from django.conf import settings

from api.view_utils import broadcast_message, ProcessedRequest, error_message
from bindings.base import GseError
from bindings import gsevol as Gse
from bindings import urec as Urec


class GseTask(Task):
    """
    Supports two ways of launching tasks and communicating results:

    ** Async: delegate task to celery and send results via websocket.
    ** Traditional: run task directly, send results in http response.
    """
    required_params = []
    variable_translations = {}

    def __init__(self, request=None):
        Task.__init__(self)
        if request:
            self.req = ProcessedRequest(request)
            print self.req
        else:
            print "nope"

    def deploy(self):
        try:
            self.prepare()
            if settings.DELEGATE_TASKS:
                self.delay()
            else:
                result = self.core()
                self.send_result(result)
        except (GseError, AssertionError) as exc:
            self.send_error(error_message(exc))

    def send_result(self, data):
        broadcast_message(data, self.req.socket)

    def send_error(self, message):
        self.send_result({"error": message})

    def run(self):
        result = self.core()
        self.send_result(result)

    def prepare(self):
        self.req.check_required_params(self.required_params)
        self.params = self.other_params
        for param in self.required_params:
            self.params[param] = self.req.params[param]
        for task_name, binding_name in self.variable_translations.items():
            self.params[binding_name] = self.params.pop(task_name)

    def core(self):
        raise NotImplemented


class DrawGene(GseTask):
    required_params = ("gene",)
    other_params = {"options": ""}
    variable_translations = {"gene": "tree"}
    def core(self):
        gtree = Gse.draw_single_tree(**self.params)
        return {"gene": gtree}

class DrawSpecies(GseTask):
    required_params = ("species",)
    other_params = {"options": ""}
    variable_translations = {"species": "tree"}
    def core(self):
        stree = Gse.draw_single_tree(**self.params)
        return {"species": stree}

class DrawMapping(GseTask):
    required_params = ("gene", "species")
    other_params = {"options": ""}
    def core(self):
        mapping = Gse.draw_mapping(**self.params)
        return {"mapping": mapping}

class AllScenarios(GseTask):
    required_params = ("gene", "species")
    other_params = {"options": ""}
    def core(self):
        return {"scenarios": Gse.scenarios(**self.params)}

class Scenario(GseTask):
    required_params = ("species", "scen")
    other_params = {"options": "", "name": "scenario"}
    def core(self):
        scen = self.params["scen"]
        d, l = Gse.scenario_cost(scen)
        return {
            self.params["name"]: {
            'scen': scen,
            'pic' : Gse.draw_embedding(self.params["species"], scen),
            'cost': {'dups': d, 'losses': l}
            }
        }

class OptScen(GseTask):
    required_params = ("gene", "species")
    other_params = {"options": ""}
    def core(self):
        optimal = Gse.optscen(**self.params)
        return Scenario().core(optimal, self.params["species"], "optscen")
