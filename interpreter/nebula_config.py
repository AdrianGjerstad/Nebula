#!/usr/bin/env python3

import sys
from error_stream import log as err

MIN_PYVER = (3, 0, 0)
CUR_PYVER = sys.version_info[:3]

def pyver_guard():
    for i in range(3):
        if MIN_PYVER[i] > CUR_PYVER[i]:
            err("Cannot complete action with Python " + version_string(CUR_PYVER))
            err("Required minimum: Python " + version_string(MIN_PYVER))
            sys.exit(1)

NEBULA_VERSION = (0, 1, 0)

PS1 = '\033[1m\033[32msnd\033[0m\033[1m>\033[0m '
PS2 = '\033[1m\033[32mcont\033[0m '
PSR = '\033[1m\033[30mret\033[0m\033[1m<\033[0m '
PSE = '\033[1m\033[31merr\033[0m\033[1m<\033[0m '

PS_TOK = '\033[1m\033[33mtok\033[0m\033[1m>\033[0m '
PS_AST = '\033[1m\033[33mast\033[0m\033[1m>\033[0m '

def version_string(ver_tuple):
    result = ""

    for i in range(len(list(ver_tuple))):
        result += ver_tuple[i]
        result += "."

    result = result[:-1]

    return result
