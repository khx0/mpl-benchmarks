#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-02-21
# file: mpl_string_formatter.py
# tested with python 3.7.6 in conjunction with mpl version 3.3.4
##########################################################################################

def cleanFormatter(x, pos = None):
    '''
    will format 0.0 as 0 and
    will format 1.0 as 1
    '''
    return '{:g}'.format(x)

def str_format_power_of_ten(text: str) -> str:
    '''
    Assumes a scientific formatted input string of the type 1.27e-05
    and will output $1.27 x 10^{-5}$ with proper power of ten formatting.
    '''
    index = text.index('e')
    mantisse, exponent = text[:index], text[(index + 1):]
    exponent = exponent.lstrip('0+') # strip learding plus sign and zeros from the exponent
    label = mantisse + r'$ \times\mathdefault{10^{' +  exponent + '}}$'
    return label

def str_format_power_of_ten_exponent(text):
    '''
    Assumes a scientific formatted input string of the type 1.27e-05
    and will output the exponent only, e.g. $x 10^{-5}$ with proper power of ten formatting.
    '''
    index = text.index('e')
    exponent = text[(index + 1):]
    label = r'$\mathdefault{\times \, 10^{' +  exponent + '}}$'
    return label

if __name__ == '__main__':

    pass
