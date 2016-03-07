# -*- coding: utf-8 -*
"""
Module for handling style options.
"""
import json
from styling.models import Option

# KINDS =


def get_available_options(kind):
    return Option.objects.filter(**{kind: True, "html_input": "number"})

def rendering_task(tree_kind):
    from bindings import tasks
    task_for_kind = {
        "gene": tasks.DrawGene,
        "species": tasks.DrawSpecies,
        "mapping": tasks.DrawMapping,
        "optscen": tasks.OptScen,
        "scenario": tasks.Scenario,
        "unrooted": tasks.DrawUnrooted,
        # TODO: diagram
    }
    assert tree_kind in task_for_kind.keys(), "Wrong tree kind"
    return task_for_kind[tree_kind]


def clean_options(kind, config):
    # Filter config for options available for given tree type
    # TODO
    return config


def stringify_options(config):
    """Convert config dict to params for gsevol, like: opt=val;opt2=val2
    """
    opts = []
    for opt, value in config.items():
        opts.append("%s=%s" % (opt, value))
    return ";".join(opts)

def make_options(kind, config):
    cleaned = clean_options(kind, config)
    return stringify_options(cleaned)

