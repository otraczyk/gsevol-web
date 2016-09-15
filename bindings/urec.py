# -*- coding: utf-8 -*-
"""Bindings related to unrooted recocilation.
Using `fasturec` and `gsevol`.
"""
import tempfile
from collections import defaultdict

from bindings.base import launch
from bindings import gsevol as Gse
from bindings.utils import wrap_in_tempfile


def launch_fasturec(params, timeout=300, stdin=None, *args, **kwargs):
    return launch(['lib/fasturec/fasturec'], params, timeout, stdin, *args, **kwargs)

def launch_urec(params, timeout=300, stdin=None, *args, **kwargs):
    return launch(['lib/urec/urec'], params, timeout, stdin, *args, **kwargs)

def draw_unrooted(gene, species, cost, options=''):
    assert cost in ("DL", "D", "L", "DC", "RF"), "Wrong cost function: %s" % cost
    fu_command = ['-g %s' % gene, '-s %s' % species, '-bX%s' % cost]
    fu_output = launch_fasturec(fu_command)
    fu_out_file = wrap_in_tempfile(fu_output)
    # Fasturec and gsevol outputs interfere and damage the picture if it's
    # printed to stdout.
    tmp = tempfile.NamedTemporaryFile()
    gse_command = ['-dSz', '-C arrowlength=0.4;scale=2;outputfile="%s"; %s' % (tmp.name, options)]
    Gse.launch(gse_command, stdin=fu_out_file)
    gse_output = tmp.read()
    return gse_output

def optimal_rootings(gene, species, cost):
    """Generate a list of representations of optimal rootings of a gene tree
    for given cost function (default=...?).
    """
    cost_to_opt = defaultdict(lambda: "a5", {
        "DL": "a8",
    })
    command = ['-g %s' % gene, '-s %s' % species, '-b', '-%s' % cost_to_opt[cost]]
    output = launch_urec(command)
    rootings = [r.strip() for r in output.strip().split('\n')]
    return rootings
