# -*- coding: utf-8 -*-
"""Bindings related to unrooted recocilation.
Using `fasturec` and `gsevol`.
"""
import subprocess
import time
import tempfile
from exceptions import RuntimeError

from api import bindings as Gse
from api.utils import wrap_in_tempfile


def launch_fasturec(params, timeout=300, stdin=None, *args, **kwargs):
    return Gse.launch(['fasturec/fasturec'], params, timeout, stdin, *args, **kwargs)

def draw_unrooted(gene, species):
    fu_command = ['-g %s' % gene, '-s %s' % species, '-bXRF']
    fu_output = launch_fasturec(fu_command)
    fu_out_file = wrap_in_tempfile(fu_output)
    # Fasturec and gsevol outputs interfere and damage the picture if it's
    # printed to stdout.
    tmp = tempfile.NamedTemporaryFile()
    gse_command = ['-dSz', '-C arrowlength=0.4;outputfile="%s"' % tmp.name]
    Gse.launch_gse(gse_command, stdin=fu_out_file)
    gse_output = tmp.read()
    return gse_output


def test():
    gene, species = Gse.random_trees().split("\n")[:2]
    return draw_unrooted(gene.strip(), species.strip())
