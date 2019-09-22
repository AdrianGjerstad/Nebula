#!/usr/bin/env python3

import sys
import nebula_config
import traceback

import nebula_arguments

import readline

# Python3 Version Guard
nebula_config.pyver_guard()
# End Python3 Version Guard

def my_except_hook(exctype, value, tb):
    sys.stderr.write('\nTraceback (most recent call last):\n')
    traceback.print_tb(tb, file=sys.stderr)
    if len(value.args) != 0:
        sys.stderr.write('%s: %s\n' % (exctype.__name__, value))
    else:
        sys.stderr.write('%s\n' % (exctype.__name__))

    sys.exit(1)

sys.excepthook = my_except_hook

def display_error(text):
    sys.stderr.write("%s%s\n" % (nebula_config.PSE, text))

def main(argc, argv):

    args, files = nebula_arguments.parse_args(argv, {
        "-v": 0, "--verbose": 0,
        "--debug": 0
    })

    ctrlc = False
    while True:
        try:
            code = input(nebula_config.PS1)
        except KeyboardInterrupt:
            if not ctrlc:
                ctrlc = True
            else:
                sys.stderr.write("Ctrl+C\nKeyboard interrupt ... stopping.\n")
                break
            sys.stderr.write("Ctrl+C\nPress Ctrl+C again, run !exit, or press Ctrl+D (EOF)\n")
            continue
        except EOFError:
            sys.stderr.write("Ctrl+D\nEnd of input ... stopping.\n")
            break

        ctrlc = False

        code = code.strip()

        if code.startswith('!'):
            code = code[1:]

            arglist = [""]
            str_esc = None
            chr_esc = False
            for i in range(len(code)):
                if code[i] == " " and str_esc is None:
                    arglist.append("")
                    continue

                if chr_esc:
                    chr_esc = False
                    if code[i] == "n":
                        arglist[len(arglist)-1] += "\n"
                    elif code[i] == "t":
                        arglist[len(arglist)-1] += "\t"
                    elif code[i] == "r":
                        arglist[len(arglist)-1] += "\r"
                    else:
                        arglist[len(arglist)-1] += code[i]
                    continue

                if code[i] == "\\":
                    chr_esc = True
                    continue

                if code[i] == "\"":
                    if str_esc is None:
                        str_esc = "\""
                        continue
                    elif str_esc == "\"":
                        str_esc = None
                        continue
                elif code[i] == "'":
                    if str_esc is None:
                        str_esc = "'"
                        continue
                    elif str_esc == "'":
                        str_esc = None
                        continue

                arglist[len(arglist)-1] += code[i]

            param_count = len(arglist) - 1
            # arglist is now an argument list split as if it was from the command prompt
            if arglist[0] == "exit":
                if param_count == 1:
                    try:
                        if int(arglist[1]) >= 0 and int(arglist[1]) <= 255:
                            return int(arglist[1])
                        else:
                            display_error("nbsh: !exit: Argument 1 must be in range [0-255]")
                    except ValueError:
                        display_error("nbsh: !exit: Argument 1 must be of type 'int'")
                elif param_count == 0:
                    return 0
                else:
                    display_error("nbsh: !exit: Requires 0-1 arguments (not %i)" % (param_count))
            elif arglist[0] == "verbosity":
                if param_count == 1:
                    if arglist[1].lower() == "on" or arglist[1].lower() == "yes" or arglist[1].lower() == "y" or arglist[1].lower() == "true" or arglist[1].lower() == "t":
                        args["-v"] = True
                    elif arglist[1].lower() == "off" or arglist[1].lower() == "no" or arglist[1].lower() == "n" or arglist[1].lower() == "false" or arglist[1].lower() == "f":
                        args["-v"] = False
                    else:
                        display_error("nbsh: !verbosity: Argument 1 must be one of [on, off, yes, no, y, n, true, false, t, f]")
                elif param_count == 0:
                    verbosity = "ON" if args["-v"] or args["--verbose"] else "OFF"
                    print("%s\033[1m\033[34mVERBOSITY: %s\033[0m" % (nebula_config.PSR, verbosity))
                else:
                    display_error("nbsh: !verbosity: Requires 0-1 arguments (not %i)" % (param_count))
            else:
                display_error("nbsh: !%s: Invalid Nebula shell command" % (arglist[0]))

    return 0

if __name__ == "__main__":
    sys.exit(main(len(sys.argv), sys.argv) or None)
