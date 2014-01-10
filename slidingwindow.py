#!/usr/bin/python
"""
Outputs the results of a sliding window over a set of lines.

For instance, with these 4 lines:

  foo
  bar
  baz
  qux

and a window size of 3, and a delimiter of $, it will output...

  foo
  foo$bar
  foo$bar$baz
  bar$baz$qux
  baz$qux
  qux

"""
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Outputs the results of a sliding window over a set of lines.")
    parser.add_argument("window", type=int,
        help="The size of the sliding window, in lines.")
    parser.add_argument("-d", "--delimiter", default=";",
        help="The delimiter to put between input lines in an output line.")
    parser.add_argument("-e", "--exact", action="store_true",
        help="Only output full sliding windows (don't output shorter at start/end).")
    args = parser.parse_args()

    window = []
    for line in sys.stdin:
        window = window[1-args.window:] if args.window > 1 else []
        window.append(line.rstrip("\n"))
        if args.exact and args.window != len(window):
            continue
        print args.delimiter.join(window)

    if args.exact:
        return

    while len(window) > 1:
        window = window[1:]
        print args.delimiter.join(window)


if __name__ == "__main__":
    main()

# vim: set ts=4 sts=4 sw=4 et:
