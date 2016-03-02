# -*- coding: utf-8 -*-

from bindings.base import launch as base_launch
from bindings.utils import wrap_in_tempfile


def launch(params, timeout=300, stdin=None, *args, **kwargs):
    command = ['python2', 'gsevol2013/src/gsevol.py']
    return base_launch(command, params, timeout, stdin, *args, **kwargs)


def random_trees():
    """
    Generate random gene and species trees with leaves a-f.
    """
    command = ['-g &randbin(a-h)', '-s &randbin(a-h)', '-egsG']
    trees = launch(command)
    gene, species = trees.split("\n")[:2]
    return gene.strip(), species.strip()


def split_to_pictures(source):
    """Divide svg source stream into pictures.

    Splits input on <?xml .*> headings.
    """
    return source.split('<?xml version="1.0" encoding="UTF-8"?>\n')[1:]


def draw_single_tree(tree, options=''):
    return launch(['-g %s' % tree, '-dgS', '-C outputfile="/dev/stdout";%s' % options])


def draw_trees(gene, species):
    """
    Draw basic output for a tree pair: gene tree and species tree.
    """
    command = ['-g %s' % gene, '-s %s' % species, '-dgsS',
               '-C outputfile="/dev/stdout"']
    source = launch(command)
    return split_to_pictures(source)

def draw_mapping(gene, species, options=''):
    """
    Draw LCA mapping for a tree pair.
    """
    command = ['-g %s' % gene, '-s %s' % species, '-dmS',
               '-C outputfile="/dev/stdout";%s' % options]
    source = launch(command)
    return split_to_pictures(source)


def scenarios(gene, species):
    """List all possible evolutionary scenarios for a pair of trees.

    Order: optimal to worst.
    """
    command = ['-g %s' % gene, '-s %s' % species, '-eGa']
    scenarios = launch(command, timeout=100).strip().split('\n')
    scenarios.reverse()
    return scenarios


def optscen(gene, species):
    """Generate optimal evolutionary scenario for the tree pair.

    Separated from scenarios(), which can be slow for larger trees.
    """
    command = ['-g %s' % gene, '-s %s' % species, '-eGn']
    scenario = launch(command).strip()
    return scenario


def draw_embedding(species, scenario):
    """
    Return svg source for embedding of a species tree into given scenario.
    """
    command = ['-t %s' % scenario, '-s %s' % species, '-de',
               '-C outputfile="/dev/stdout";scale=2.5']
    return launch(command)


def draw_diagram(gene, species):
    """Draw reduction diagram for a pair of trees.

    - Generate 'fat scenario', format species and the scenario as '.gse' script.
    - Pass output to gsevol once again to draw diagram.
    """
    scen_command = ['-g %s' % gene, '-s %s' % species, '-esfG', '-vp']
    scen_output = launch(scen_command)
    scen_file = wrap_in_tempfile(scen_output)
    diag_command = ['-dd', '-C outputfile="/dev/stdout"']
    diag_output = launch(diag_command, stdin=scen_file, timeout=1200)
    return diag_output

def scenario_cost(scenario):
    command = ['-t %s' % scenario, '-cc']
    dups, losses = launch(command).split(' ')[:2]
    return dups, losses
