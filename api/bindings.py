# -*- coding: utf-8 -*-
import subprocess
import time
from exceptions import RuntimeError

from django.conf import settings

class GseError(Exception):
    pass


def launch(params, timeout=300):
    """Launch Gsevol subprocess.

    Basic implementation: gsevol is launched in a subprocess,
    given a time limit (default 300 seconds).

    :param params: a list of parameters which will be passed by the
        command line. Includes input data, flags and special '&'-commands
    :param timeout: time limit for the process in seconds

    If the process ends successfully, returns the output from stdout.
    """
    gse_process = subprocess.Popen(
        settings.GSEVOL_COMMAND.split(' ') + params,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    timer = time.time() + timeout
    while gse_process.poll() is None:
        if time.time() > timer:
            gse_process.terminate()
            raise RuntimeError("Gsevol process timeout", params)
    out, err = gse_process.communicate()
    if err:
        raise GseError("Gsevol error", err, params, out)
    return out

def launch_command(command):
    """
    Launches Gsevol with given command string.
    """
    out = launch(command)
    return out

def random_trees():
    """
    Generate random gene and species trees with leaves a-f.
    """
    command = ['-g &randbin(a-f)', '-s &randbin(a-f)', '-egsG']
    return launch_command(command)

def draw_randbin_s():
    """
    Demo: return random tree svg.
    """
    svg_source = launch_command(
        '-g &randbin(a-f) -s &randbin(a-f) -dgS -C outputfile="/dev/stdout"'
    )
    return svg_source

def split_to_pictures(source):
    """Divide svg source stream into pictures.

    Splits input on <?xml .*> headings.
    """
    return source.split('<?xml version="1.0" encoding="UTF-8"?>\n')[1:]

def draw_single_tree(tree):
    return launch_command(['-g %s' % tree, '-dgS', '-C outputfile="/dev/stdout"'])

def draw_trees(gene, species):
    """
    Draw basic output for a tree pair: gene tree, species tree and their mapping.
    """
    command = ['-g %s' % gene, '-s %s' % species, '-dgsmS',
               '-C outputfile="/dev/stdout"']
    source = launch_command(command)
    return split_to_pictures(source)

def scenarios(gene, species):
    """
    List all possible evolutionary scenarios for a pair of trees.

    Order: optimal to worst.
    """
    command = ['-g %s' % gene, '-s %s' % species, '-eGa']
    scenarios = launch_command(command).strip().split('\n')
    scenarios.reverse()
    return scenarios

def optscen(gene, species):
    """
    Generate optimal evolutionary scenario for the tree pair.
    """
    command = ['-g %s' % gene, '-s %s' % species, '-eGn']
    scenario = launch_command(command).strip()
    return scenario

def draw_embedding(species, scenario):
    """
    Return svg source for embedding of a species tree into given scenario.
    """
    command = ['-t %s' % scenario, '-s %s' % species, '-de',
               '-C outputfile="/dev/stdout";scale=2.5']
    return launch_command(command)

