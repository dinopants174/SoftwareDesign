# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 22:59:22 2014

@author: zoherghadyali
"""

from random import randint
from math import *
import Image

def build_random_function(min_depth, max_depth):
    # your doc string goes here

    # your code goes here
    l = ["x","y"]
    funcs = ["sin_pi", "cos_pi", "square", "prod", "avg"]
    depth = randint(min_depth, max_depth)
    if depth == 1:
        return [l[randint(0,1)]]
    elif depth>1:
        rand_func = funcs[randint(0,4)]
        if rand_func in funcs[0:3]:
            return [rand_func, build_random_function(depth-1, depth-1)]
        elif rand_func in funcs[3:]:
            return [rand_func, build_random_function(depth-1, depth-1), build_random_function(depth-1, depth-1)]

f = build_random_function(1,3)

def evaluate_random_function(f, x, y):
    # your doc string goes here

    # your code goes here
    if f[0] == "x":
        return x
    elif f[0] == "y":
        return y
    elif f[0] == "sin_pi":
        return sin(pi*evaluate_random_function(f[1], x, y))
    elif f[0] == "cos_pi":
        return cos(pi*evaluate_random_function(f[1], x, y))
    elif f[0] == "square":
        return evaluate_random_function(f[1], x, y)**2
    elif f[0] == "prod":
        return evaluate_random_function(f[1], x, y) * evaluate_random_function(f[2], x, y)
    elif f[0] == "avg":
        return (evaluate_random_function(f[1], x, y) + evaluate_random_function(f[2], x, y))/2.0
    
#def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ Maps the input value that is in the interval [input_interval_start, input_interval_end]
        to the output interval [output_interval_start, output_interval_end].  The mapping
        is an affine one (i.e. output = input*c + b).
    
        TODO: please fill out the rest of this docstring
    """
    # your code goes here

if __name__ == '__main__':
    print f
    print evaluate_random_function(f,5,5)