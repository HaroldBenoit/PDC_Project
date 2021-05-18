# -*- coding: utf-8 -*-
"""
Created on Tue May 18 11:02:04 2021

@author: Harold
"""
import numpy as np




def main():
    input= '!@@@@@@#°§¬|¢¢0idashfia'
    encoded = string2real(input)
    decoded= real2string(encoded)
    
def channel(chanInput):
    chanInput = np.clip(chanInput,-1,1)
    erasedIndex = np.random.randint(3)
    chanInput[erasedIndex:len(chanInput):3] = 0
    return chanInput + np.sqrt(10)*np.random.randn(len(chanInput))


def string2real(input):
    print('\n@@@@@@@@@@@@@@@@@@@@@@@ENCODING@@@@@@@@@@@@@@@@@@@@@@@\n')
    
    print('starting string :',input,'\n')
    
    arr = np.array(bytearray(input, 'utf-8')).astype('float64')
    print(arr)
    arr = (arr -128)
    print(arr)
    arr = arr/255
    print(arr)
    return arr

    

def real2string(arr):
    print('\n@@@@@@@@@@@@@@@@@@@@@@@DECODING@@@@@@@@@@@@@@@@@@@@@@@\n')
    arr = ((arr*255) + 128).astype('byte')
    print(arr)
    arr = bytearray(arr)
    print(arr,'\n')
    string= str(arr,'utf-8')
    print('result string:',string)
    
main()