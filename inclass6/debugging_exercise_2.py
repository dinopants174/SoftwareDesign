# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 17:52:54 2014

@author: pruvolo
"""

def factorial(n):
    """ Computes the factorial of the non-negative input integer n """
    return_val = 1
    for i in range(n):
        #print "In loop, value of i is " + str(i)
        return_val *= i
        assert(return_val >= 1)
    return return_val

if __name__ == '__main__':
    print factorial(5)