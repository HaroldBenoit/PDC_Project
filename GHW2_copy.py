# -*- coding: utf-8 -*-
"""
Created on Tue May 18 22:59:12 2021

@author: Harold
"""

import numpy as np


def main():
    input= 'asda@¦#°#@°@§#@#§hfasugvbvavàé¨é'
    encoded = encode(input)
    encoded_loss = easyChannel(encoded)
    decoded = decode(encoded_loss)
    print(decoded)
    print(decoded==input)
    
"""
Noisy channel
"""    
def channel(chanInput):
    chanInput = np.clip(chanInput,-1,1)
    erasedIndex = np.random.randint(3)
    chanInput[erasedIndex:len(chanInput):3] = 0
    return chanInput + np.sqrt(10)*np.random.randn(len(chanInput))

"""
Noiseless channel
"""
def easyChannel(chanInput):
    chanInput = np.clip(chanInput,-1,1)
    erasedIndex = np.random.randint(3)
    chanInput[erasedIndex:len(chanInput):3] = 0
    return chanInput
    
"""
Takes an input in [0,3] and returns the corresponding codeword

"""
def create_code(i):
    codebook = {0:[1,1,1],1:[1,-1,-1],2:[-1,1,-1],3:[-1,-1,1]}
    return np.array(codebook[i])



def get2bits(num):
     bits = []
     bits.append(num >> 6) ## get first 2 bits
     bits.append((num & 48) >> 4) # get second 2 bits
     bits.append((num & 12) >> 2) 
     bits.append(num & 3)

     return bits

"""

"""
def encode(input):
    arr = np.array(bytearray(input, 'utf-8')).astype('int')
    output = np.empty
    for i in range(len(arr)):
        num = arr[i]
        bits = get2bits(num)
        for j in range(4):
            output = np.hstack((output,create_code(bits[j])))
        
    #remove empty in the beginning
    return output[1:]

def recover_codeword(arr):
    if(len(arr) != 3):
        raise ValueError("array doesn't have length 3")
        
    if arr[0] == 0:
        if arr[1] == 1:
            if arr[2] == 1:
                return 0
            else:
                return 2
        else:
            if arr[2] == 1:
                return 3
            else:
                return 1
            
    elif arr[1] == 1:
        
    else:
        

"""
This function takes a 1D np.array of size 2k*256 such that the array represents
2 times repeated codewords of length 256.  
"""
def decode_noiseless(input):
    output = []
    
    for i in range(0,len(input),3):
        
        
        if value < 256:
            output.append(value)
        else:
            output.append(value-256)
            
    return str(bytearray(output),'utf-8')
        