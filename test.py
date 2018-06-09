#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 00:25:49 2018

@author: meyerhof
"""
import os

def rearrange(num):

    global pages
    pages = []
    cycle = num//4
    rest = num%4
    assert rest < 4    

    a = 4
    b = 1
    c = 2
    d = 3


    for i in range(1,cycle+1):
        pages.append(a)
        pages.append(b)
        pages.append(c)
        pages.append(d)
        a = a + 4
        b = b + 4
        c = c + 4
        d = d + 4

    if (rest != 0) and (num > 4):
        begin = pages[-4] +1
        end = pages[-4] + rest
        #print(begin, end)
        pages.append(0)
    
        for i in range (begin, end+1):
            pages.append(i)
    
    elif 0 < num <= 4:
        pages.append(0)
        for i in range(1,num+1):
            pages.append(i)
    
    elif num == 0:
        pages = []

paths = []        
for i in pages:
    i = str(i)
    temp = 'fw9_page_' + i + '.pdf'
    paths.append(temp)


print(paths)
#if __name__ == '__main__':
 #   paths = glob.glob('fw9_page_1.pdf')
  #  print(paths)
   # print()
#    paths.sort()
 #   print(paths)