# -*- coding: utf-8 -*-
"""
Created on Tue May 18 11:02:04 2021

@author: Harold
"""
import numpy as np




def main():
    string2bits('hello')
    
    
def channel(chanInput):
    chanInput = np.clip(chanInput,-1,1)
    erasedIndex = np.random.randint(3)
    chanInput[erasedIndex:len(chanInput):3] = 0
    return chanInput + np.sqrt(10)*np.random.randn(len(chanInput))


def string2bits(input):
    arr = np.array(bytearray(input, 'utf-8'))
    print(arr)
    
main()