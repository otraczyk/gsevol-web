# -*- coding: utf-8 -*
"""
Module for handling style options.
"""
import json
from styling.models import Option

KINDS = ['unrooted', 'scenario', 'mapping', 'optscen', 'gene', 'species', 'diagram']

def get_available_options(kind):
    assert kind in KINDS, "Wrong tree kind %s" % kind
    if kind == 'optscen':
        kind = 'scenario'
    return Option.objects.filter(**{kind: True})

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
    filtered_config = {}
    available = get_available_options(kind)
    for opt in available:
        if config.get(opt.name) is not None:
            try:
                value = opt.fix_type(config.get(opt.name))
            except ValueError:
                print "type: rejected", opt.name, config[opt.name]
                continue
            if opt.valid(value):
                filtered_config[opt.name] = value
                del config[opt.name]
            else:
                print "scope: rejected", opt.name, value
    # TODO: change prints to logged warnings?
    return filtered_config


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

