# -*- coding: utf-8 -*-
import tempfile

def wrap_in_tempfile(data):
    """Return SpooledTemporaryFile with given data as content, ready to read
    eg. as a subprocess input.
    """
    wrapped = tempfile.SpooledTemporaryFile()
    wrapped.write(data)
    wrapped.flush()
    wrapped.seek(0)
    return wrapped
