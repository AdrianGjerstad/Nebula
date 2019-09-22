#!/usr/bin/env python3

import sys

def log(*values, end="\n", sep=" "):
    result = ""

    values = list(values)

    for i in range(len(values)):
        result += values[i]
        result += sep

    result = result[:-1*len(sep)]

    result += end

    sys.stderr.write(result)
    sys.stderr.flush()
