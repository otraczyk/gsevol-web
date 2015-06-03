# -*- coding: utf-8 -*-
import subprocess
import time
from exceptions import RuntimeError

from django.conf import settings


def launch(params, timeout=300):
    """
    Basic implementation: gsevol is launched in a subprocess, 
    given a time limit (default 300 seconds).

    :param params: a list of parameters which will be passed by the
        command line. Includes input data, flags and special '&'-commands
    :param timeout: time limit for the process in seconds

    If the process ends successfully, returns the output file handle 
    from stdout.
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
    if gse_process.returncode != 0:
        out, err = gse_process.communicate()
        raise RuntimeError("Gsevol error", err, params)

    return gse_process.stdout


def gen_randbin_f():
    """
    Demo: generates random binary gene and species trees with leaves a-f.
    """
    command = '-g &randbin(a-f) -s &randbin(a-f) -egsG'
    out = launch(command.split(' '))
    return out.read()
