#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Plotting terminal based scatterplots
"""

from __future__ import print_function
import csv
import sys
import optparse
from email.policy import default
from pydoc import describe

from .utils.helpers import *
from .utils.commandhelp import scatter


def get_scale(series, is_y=False, steps=20):
    min_val = min(series)
    max_val = max(series)
    scaled_series = []
    for x in drange(min_val, max_val, (max_val - min_val) / steps,
                    include_stop=True):
        if x > 0 and scaled_series and max(scaled_series) < 0:
            scaled_series.append(0.0)
        scaled_series.append(x)

    if is_y:
        scaled_series.reverse()
    return scaled_series


def _plot_scatter(xs, ys, size, pch, colour, title, title_align, cs, xtitle, ytitle):
    plotted = set()
    width = len(get_scale(xs, False, size))
    xscale = get_scale(xs,False,size)

    if title:
        print(box_text(title, title_align, 2 * (width + 1)))

    if ytitle:
        print("y: " + ytitle)

    print("-" * (2 * (width + 2)))
    for y in get_scale(ys, True, size):    #y axis loop
        print("|", end=' ')

        for x in get_scale(xs, False, size): #x axis loop
            point = " "
            for (i, (xp, yp)) in enumerate(zip(xs, ys)):
                if xp <= x and yp >= y and (xp, yp) not in plotted:
                    point = pch
                    plotted.add((xp, yp))       # add the point on the graph
                    if cs:
                        colour = cs[i]
            #printcolour(point + " ", True, colour)

            if point == pch:
                printcolour(point + " ", True, colour)
            else:
                if x == 0  and y == 0:
                    printcolour("o ", True, colour)
                elif y == 0:
                    printcolour("- ", True, colour)
                elif x == 0:
                    printcolour("| ", True, colour)
                else:
                    printcolour(point + " ", True, colour)


        print(" |")
    print("-" * (2 * (width + 2)))

    if xtitle:
        print(str("x: " + xtitle).rjust(width))

def plot_scatter(f, xs, ys, size, pch, colour, title, title_align="center", xtitle="", ytitle=""):
    """
    Form a complex number.

    Arguments:
        f -- comma delimited file w/ x,y coordinates
        xs -- if f not specified this is a file w/ x coordinates
        ys -- if f not specified this is a filew / y coordinates
        size -- size of the plot
        pch -- shape of the points (any character)
        colour -- colour of the points
        title -- title of the plot
        title_align -- alignment for the title of the plot
        xtitle -- title for x-axis
        ytitle -- title for y-axis
    """
    cs = None
    if f:
        if isinstance(f, str):
            with open(f) as fh:
                data = [tuple(line.strip().split(',')) for line in fh]
        else:
            data = [tuple(line.strip().split(',')) for line in f]
        xs = [float(i[0]) for i in data]
        ys = [float(i[1]) for i in data]
        if len(data[0]) > 2:
            cs = [i[2].strip() for i in data]
    elif isinstance(xs, list) and isinstance(ys, list):
        pass
    else:
        with open(xs) as fh:
            xs = [float(str(row).strip()) for row in fh]
        with open(ys) as fh:
            ys = [float(str(row).strip()) for row in fh]

    _plot_scatter(xs, ys, size, pch, colour, title, title_align, cs, xtitle, ytitle)
    


def main():

    parser = optparse.OptionParser(usage=scatter['usage'])

    parser.add_option('-f', '--file', help='a csv w/ x and y coordinates', default=None, dest='f')
    parser.add_option('-t', '--title', help='title for the chart', default="", dest='t')
    parser.add_option('-x', help='x coordinates', default=None, dest='x')
    parser.add_option('-y', help='y coordinates', default=None, dest='y')
    parser.add_option('-s', '--size', help='y coordinates', default=20, dest='size', type='int')
    parser.add_option('-p', '--pch', help='shape of point', default="x", dest='pch')
    parser.add_option('-c', '--colour', help='colour of the plot (%s)' %
                      colour_help, default='default', dest='colour')
    parser.add_option('--xtitle', help='title for x-axis of graph', default='', dest='xtitle')
    parser.add_option('--ytitle', help='title for y-axis of graph', default='', dest='ytitle')

    opts, args = parser.parse_args()

    if opts.f is None and (opts.x is None or opts.y is None):
        opts.f = sys.stdin.readlines()

    if opts.f or (opts.x and opts.y):
        plot_scatter(opts.f, opts.x, opts.y, opts.size, opts.pch, opts.colour, opts.t)
    else:
        print("nothing to plot!")


if __name__ == "__main__":
    main()
