# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 23:50:55 2014

@author: zoherghadyali
"""
#Exercise 5.3 fermat.py
#SoftwareDesign 2014

def check_fermat(a,b,c,n):
    if n>2 and a**n + b**n == c**n:
        print "Holy smokes, Fermat was wrong!"
    else:
        print "No, that doesn't work"


a = raw_input("Please enter the value you would like to use for a: ")
b = raw_input("Please enter the value you would like to use for b: ")
c = raw_input("Please enter the value you would like to use for c: ")
n = raw_input("Please enter the value you would like to use for n: ")

a = int(a)
b = int(b)
c = int(c)
n = int(n)

check_fermat(a,b,c,n)