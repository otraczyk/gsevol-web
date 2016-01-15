import subprocess
import tempfile
import time


class GseError(Exception):
    pass


def launch(command, params, timeout=300, stdin=None, *args, **kwargs):
    """Launch an external tool (gsevol, fasturec...) as a subprocess.

    Basic implementation: gsevol is launched in a subprocess,
    given a time limit (default 300 seconds).

    :param command: program name as a list of strings to pass to the command line
    :param params: a list of parameters which will be passed by the
        command line. Includes input data, flags and special '&'-commands
    :param timeout: time limit for the process in seconds

    If the process ends successfully, returns the output from stdout.
    """
    if stdin:
        # HACK: There's problem (deadlocks?) with receiving stdout when sending
        # something via stdin. On the other hand, I couldn't get multiple
        # pictures written to one tempfile. Enough time wasted here.
        output = tempfile.NamedTemporaryFile()
    else:
        output = subprocess.PIPE

    gse_process = subprocess.Popen(
        command + params,
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
