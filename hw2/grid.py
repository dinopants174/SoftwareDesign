# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 23:34:10 2014

@author: zoherghadyali
"""
#Exercise 3.5 grid.py
#SoftwareDesign 2014

def grid_plus_dash():
    x = "+ - - - - "
    print 2*x + "+"

def grid_dash():
    y = "|         "
    print 2*y + "|"
    
def print_grid_dash():
    grid_dash()
    grid_dash()
    grid_dash()
    grid_dash()


grid_plus_dash()
print_grid_dash()
grid_plus_dash()
print_grid_dash()
grid_plus_dash()

def grid_plus_dash_4():
    x = "+ - - - - "
    print 4*x + "+"

print ""
print ""

def grid_dash_4():
    y = "|         "
    print 4*y + "|"
    
def print_grid_dash_4():
    grid_dash_4()
    grid_dash_4()
    grid_dash_4()
    grid_dash_4()


grid_plus_dash_4()
print_grid_dash_4()
grid_plus_dash_4()
print_grid_dash_4()
grid_plus_dash_4()
print_grid_dash_4()
grid_plus_dash_4()
print_grid_dash_4()
grid_plus_dash_4()