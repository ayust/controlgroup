#!/usr/bin/python
"""
Converts a word search grid into a list of possible lines.
"""
import argparse
import sys

def possible_lines(grid, diagonals=True):
    height = len(grid)
    width = len(grid[0])

    # Horizontal
    for horiz in grid:
        yield "".join(horiz)

    # Vertical
    for x in xrange(width):
        yield "".join(grid[y][x] for y in xrange(height))

    if not diagonals:
        return

    # SE diagonals from top row
    for x in xrange(width):
        yield "".join(grid[i][x+i] for i in xrange(height) if x+i < width)

    # SE diagonals from left side, not including 0,0
    for y in xrange(1, height):
        yield "".join(grid[y+i][i] for i in xrange(width) if y+i < height)

    # NE diagonals from left side
    for y in xrange(height):
        yield "".join(grid[y-i][i] for i in xrange(width) if y-i >= 0)

    # NE diagonals from bottom, not including 0,height-1
    for x in xrange(1, width):
        yield "".join(grid[height-i-1][x+i] for i in xrange(height) if x+i < width)


def main():
    parser = argparse.ArgumentParser(description="Converts a word search grid into a list of lines.")
    parser.add_argument("-d", "--diagonal", action="store_true",
        help="Include diagonal lines.")
    parser.add_argument("-r", "--reverse", action="store_true",
        help="Include the reverse of each line.")
    args = parser.parse_args()

    grid = [list(line.rstrip("\n")) for line in sys.stdin]

    lines = set(possible_lines(grid, args.diagonal))
    if args.reverse:
        lines |= set("".join(reversed(line)) for line in lines)

    for line in lines:
        print line


if __name__ == "__main__":
    main()

# vim: set ts=4 sts=4 sw=4 et:
