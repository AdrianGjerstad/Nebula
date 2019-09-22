#!/usr/bin/env python3

import nebula_config

# Python3 Version Guard
nebula_config.pyver_guard()
# End Python3 Version Guard

def parse_args(argv=[], opcd={}):
    skip_count = 0

    result = {}
    uncaught = []

    for key in opcd:
        result[key] = [""]*opcd[key]
        if opcd[key] == 0:
            result[key] = False

    for i in range(1, len(argv)):
        if skip_count > 0:
            skip_count -= 1
            continue

        param_count = opcd.get(argv[i])

        if param_count is None:
            # No dictionary entry for this
            uncaught.append(argv[i])
            continue

        if param_count == 0:
            result[argv[i]] = True
            continue

        skip_count = param_count
        key = argv[i]
        result[key] = [""]*param_count

        for j in range(param_count):
            result[key][j] = argv[i+j+1]

    return (result, uncaught)
