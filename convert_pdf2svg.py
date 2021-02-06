#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-02-06
# file: convert_pdf2svg.py
# tested with python 3.7.6
##########################################################################################

import os
import datetime
from glob import glob as glob

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASEDIR, 'out_svg')

os.makedirs(OUTDIR, exist_ok = True)

def convert_pdf2svg(figures, outdir = OUTDIR):
    '''
    converts list of *.pdf figures (as contained in figures)
    to svg figures using the command line tool pdf2svg
    '''
    for figure in figures:

        outname = os.path.splitext(os.path.basename(figure))[0]

        cmd = 'pdf2svg ' + figure + \
            ' ' + os.path.join(outdir, outname + '.svg')

        os.system(cmd)

if __name__ == '__main__':

    # path to target directory containing the pdf files to be converted
    glob_search_path = r'/path/to/target/glob/dir/*.pdf'

    # create candidate figure list via globbing
    figure_list = glob(glob_search_path)

    convert_pdf2svg(figure_list,
                    outdir = OUTDIR)
