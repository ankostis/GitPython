# -*- coding: utf-8 -*-
# config.py
# Copyright (C) 2008, 2009 Michael Trier (mtrier@gmail.com) and contributors
#
# This module is part of GitPython and is released under
# the BSD License: http://www.opensource.org/licenses/bsd-license.php
"""utilities to help provide compatibility with python 3"""
# flake8: noqa

import os
import sys

from gitdb.utils.compat import (
    PY3,
    xrange,
    MAXSIZE,
    izip,
)

from gitdb.utils.encoding import (
    string_types,
    text_type,
    force_bytes,
    force_text
)

defenc = sys.getdefaultencoding()
if PY3:
    import io
    FileType = io.IOBase
    def byte_ord(b):
        return b
    def bchr(n):
        return bytes([n])
    def mviter(d):
        return d.values()
    range = xrange
    unicode = str
    binary_type = bytes
else:
    FileType = file
    # usually, this is just ascii, which might not enough for our encoding needs
    # Unless it's set specifically, we override it to be utf-8
    if defenc == 'ascii':
        defenc = 'utf-8'
    byte_ord = ord
    bchr = chr
    unicode = unicode
    binary_type = str
    range = xrange
    def mviter(d):
        return d.itervalues()


def safe_decode(s):
    """Safely decodes a binary string to unicode"""
    if isinstance(s, unicode):
        return s
    elif isinstance(s, bytes):
        return s.decode(defenc, 'replace')
    raise TypeError('Expected bytes or text, but got %r' % (s,))


def with_metaclass(meta, *bases):
    """copied from https://github.com/Byron/bcore/blob/master/src/python/butility/future.py#L15"""
    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__

        def __new__(cls, name, nbases, d):
            if nbases is None:
                return type.__new__(cls, name, (), d)
            # There may be clients who rely on this attribute to be set to a reasonable value, which is why
            # we set the __metaclass__ attribute explicitly
            if not PY3 and '___metaclass__' not in d:
                d['__metaclass__'] = meta
            # end
            return meta(name, bases, d)
        # end
    # end metaclass
    return metaclass(meta.__name__ + 'Helper', None, {})
    # end handle py2


def is_py2():
    return sys.version_info[0] < 3


def is_win():
    return os.name == 'nt'


def is_posix():
    return os.name == 'posix'


def is_darwin():
    return os.name == 'darwin'


_is_cygwin_cache = {}
def is_cygwin_git(git_executable):
    is_cygwin = _is_cygwin_cache.get(git_executable)
    if is_cygwin is None:
        is_cygwin = False
        try:
            git_dir = osp.dirname(git_executable)
            if not git_dir:
                res = py_where(git_executable)
                git_dir = osp.dirname(res[0]) if res else None

                ## Just a name given, not a real path.
            uname_cmd = osp.join(git_dir, 'uname')
            uname = check_output(uname_cmd)
            is_cygwin = 'CYGWIN' in uname
        except Exception as ex:
            log.debug('Failed checking if running in CYGWIN due to: %r', ex)
        _is_cygwin_cache[git_executable] = is_cygwin

    return is_cygwin
