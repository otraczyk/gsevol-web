# -*- coding: utf-8 -*-
import subprocess
import time
import tempfile
from exceptions import RuntimeError

from django.conf import settings

from api.utils import wrap_in_tempfile

class GseError(Exception):
    pass


def launch(params, timeout=300, stdin=None, *args, **kwargs):
    """Launch Gsevol subprocess.

    Basic implementation: gsevol is launched in a subprocess,
    given a time limit (default 300 seconds).

    :param params: a list of parameters which will be passed by the
        command line. Includes input data, flags and special '&'-commands
    :param timeout: time limit for the process in seconds

    If the process ends successfully, returns the output from stdout.
    """
    if stdin:
        # HACK: There's problem (deadlocks?) with receiving stdout when sending
        # something via stdin. On the other hand, I couldn't get multiple
        # pictures wtitten to one tempfile. Enough time wasted here.
        output = tempfile.NamedTemporaryFile()
    else:
        output = subprocess.PIPE

    gse_process = subprocess.Popen(
        ['python2', 'gsevol2013/src/gsevol.py'] + params,
        stdout=output, stderr=subprocess.PIPE, bufsize=1, stdin=stdin
    )

    timer = time.time() + timeout
    while gse_process.poll() is None:
        if time.time() > timer:
            gse_process.terminate()
            raise RuntimeError("Gsevol process timeout", params)
    out, err = gse_process.communicate()
    if err:
        raise GseError("Gsevol error", err, params, out)
    if hasattr(output, 'read'):
        return output.read()
    return out

def random_trees():
    """
    Generate random gene and species trees with leaves a-f.
    """
    command = ['-g &randbin(a-f)', '-s &randbin(a-f)', '-egsG']
    return launch(command)

def split_to_pictures(source):
    """Divide svg source stream into pictures.

    Splits input on <?xml .*> headings.
    """
    return source.split('<?xml version="1.0" encoding="UTF-8"?>\n')[1:]

def draw_single_tree(tree):
    return launch(['-g %s' % tree, '-dgS', '-C outputfile="/dev/stdout"'])

def draw_trees(gene, species):
    """
    Draw basic output for a tree pair: gene tree, species tree and their mapping.
    """
    command = ['-g %s' % gene, '-s %s' % species, '-dgsmS',
               '-C outputfile="/dev/stdout"']
    source = launch(command)
    return split_to_pictures(source)

def scenarios(gene, species):
    """List all possible evolutionary scenarios for a pair of trees.

    Order: optimal to worst.
    """
    command = ['-g %s' % gene, '-s %s' % species, '-eGa']
    scenarios = launch(command).strip().split('\n')
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
    diag_output = launch(diag_command, stdin=scen_file)
    return diag_output
