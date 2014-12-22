#!/usr/bin/python
"""
Python MapReduce - A very basic way to run mass operations on text.

Example usages:

  Basic map operation -

    $ echo -e "1\n2\n3" | ./pythonmr.py --map="int(item)*2"
    2
    4
    6

  Basic reduce operation (with initialized accumulator) -

    $ echo -e "1\n2\n3\n4" | ./pythonmr.py --reduce="int(item)+accum" --accum="0"
    10

  Without --skip, this would result in an error (due to the blank line where 3 was),
  but with it, the blank line is ignored -

    $ echo -e "1\n2\n\n4" | ./pythonmr.py --skip --reduce="int(item)+accum" --accum="0"
    10

  Combined map and reduce -

    $ echo -e "1\n2\n3\n4" | ./pythonmr.py --map="int(item)" --reduce="item+accum"
    10
"""
import argparse
import collections
import itertools
import sys

def map_python(expr, iterable, env):
    def eval_expr(item):
        return eval(expr, dict(item=item, **env))
    return itertools.imap(eval_expr, iterable)

def reduce_python(expr, iterable, initial, env):
    def eval_expr(accum, item):
        return eval(expr, dict(item=item, accum=accum, **env))
    if initial is not None:
        return reduce(eval_expr, iterable, eval(initial))
    else:
        return reduce(eval_expr, iterable)

def filter_python(expr, iterable, env):
    def eval_expr(item):
        return eval(expr, dict(item=item, **env))
    return itertools.ifilter(eval_expr, iterable)

def main():
    parser = argparse.ArgumentParser(description="Process text by running Python code as map and reduce steps.")
    parser.add_argument("-m", "--map", metavar="EXPR",
        help="A python expression to be mapped onto the input lines (use 'item' variable).")
    parser.add_argument("-s", "--skip", action="store_true",
        help="Omit falsey (None, False, empty string, etc) values after map step.")
    parser.add_argument("-r", "--reduce", metavar="EXPR",
        help="A python expression to be reduced onto the input lines (use 'accum' and 'item' variables).")
    parser.add_argument("-f", "--filter", metavar="EXPR",
        help="A python expression to be filtered onto the input lines (use 'item' variable).")
    parser.add_argument("-a", "--accum", metavar="EXPR",
        help="A python expression with which to initialize the accumulator for reduces.")
    parser.add_argument("-i", "--in", metavar="FILEPATH",
        help="A path to a file to use as input, instead of stdin.")
    parser.add_argument("-o", "--out", metavar="FILEPATH",
        help="A path to a file to use as output, instead of stdout.")
    parser.add_argument("-p", "--package", action="append", default=[],
        help="A package to import and make available in expressions (repeatable).")
    parser.add_argument("--auto", metavar="PACKAGE",
        help="A package with a 'mapper' and/or 'reducer' function defined to run.")

    args = vars(parser.parse_args())

    # Default to stdin as the data source
    if args["in"]:
        source = open(args["in"])
    else:
        source = sys.stdin

    # Default to stdout as the data sink
    if args["out"]:
        output = open(args["out"], "w")
    else:
        output = sys.stdout

    automodule = __import__(args["auto"]) if args["auto"] else None
    packages = dict((package,__import__(package)) for package in args['package'])

    # First, strip the newlines off each line of text
    result = itertools.imap(lambda line: line.rstrip("\n"), source)

    # Then, run a filter step, if specified
    if args["filter"]:
        result = filter_python(args["filter"], result, packages)
    elif hasattr(automodule, 'filterer'):
        result = itertools.ifilter(automodule.filterer, result)

    # Then, run a map step, if specified
    if args["map"]:
        result = map_python(args["map"], result, packages)
    elif hasattr(automodule, 'mapper'):
        result = itertools.imap(automodule.mapper, result)

    if args["skip"]:
        result = (item for item in result if item)

    # Then a reduce step, if specified
    if args["reduce"]:
        result = reduce_python(args["reduce"], result, args["accum"], packages)
    elif hasattr(automodule, 'reducer'):
        result = reduce(automodule.reducer, result)

    # Finally, output the result
    try:
        if isinstance(result, collections.Iterable):
            for item in result:
                if isinstance(item, collections.Iterable) and not isinstance(item, (str, unicode)):
                    item = "\t".join(map(str, item))
                output.write("%s\n" % item)
        else:
            output.write("%s\n" % result)
    except IOError:
        # To ignore 'broken pipe' errors
        pass


if __name__ == "__main__":
    main()

# vim: set ts=4 sts=4 sw=4 et:
