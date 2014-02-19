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

def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ Maps the input value that is in the interval [input_interval_start, input_interval_end]
        to the output interval [output_interval_start, output_interval_end].  The mapping
        is an affine one (i.e. output = input*c + b).
    
        TODO: please fill out the rest of this docstring
    """
    num = float((output_interval_end - output_interval_start)*(val - input_interval_start))
    denom = input_interval_end - input_interval_start    
    res = num/denom + output_interval_start    
    return res    
    
def create_image():
    red_ch = build_random_function(6,9)
    green_ch = build_random_function(6,9)
    blue_ch = build_random_function(6,9)
    
    im = Image.new("RGB", (350,350))
    pixels = im.load()
    
    for x in range(350):
        x_val = remap_interval(x, 0, 349, -1, 1)
        for y in range(350):
            y_val = remap_interval(y, 0, 349, -1, 1)
            red_val = evaluate_random_function(red_ch, x_val, y_val)
            green_val = evaluate_random_function(green_ch, x_val, y_val)
            blue_val = evaluate_random_function(blue_ch, x_val, y_val)
            red = remap_interval(red_val, -1, 1, 0, 255)
            green = remap_interval(green_val, -1, 1, 0, 255)
            blue = remap_interval(blue_val, -1, 1, 0, 255)
            pixels[int(x),int(y)] = (int(red), int(green), int(blue))
    im.show()
            
if __name__ == '__main__':
    print f
    print evaluate_random_function(f,5,5)
    print remap_interval(75, 50, 100, 0, 1)
    create_image()