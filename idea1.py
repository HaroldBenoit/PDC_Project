# -*- coding: utf-8 -*-
"""
Created on Wed May 19 10:12:11 2021

@author: Harold
"""

import numpy as np


def main():
    input= 'asda@¦#°#@°@§#@#§hfasugvbvavàé¨é'
    encoded = encode(input)
    encoded_loss = channel(encoded)
    pred = prediction(encoded_loss)
    decoded = decode_after_prediction(pred)
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
    codebook = {0:[1,1,1,1,1,1],1:[-1,-1,-1,-1,-1,-1]}
    return np.array(codebook[i])



def getbits(num):
    bits = []
    for i in range(7,-1,-1):
        bits.append((num >> i)&1)
    return bits

"""

"""
def encode(input):
    arr = np.array(bytearray(input, 'utf-8')).astype('int')
    output = np.empty
    for i in range(len(arr)):
        num = arr[i]
        bits = getbits(num)
        for j in range(8):
            output = np.hstack((output,create_code(bits[j])))
        
    #remove empty in the beginning
    return output[1:]


def decode_from_codeword(arr):
    
    if(len(arr) != 6):
        raise ValueError("wrong length, should be 6")
    
    for j in len(arr):
        if arr[j] == 1:
            return 0
        elif arr[j] == -1:
            return 1
    
    raise ValueError("array isn't a valid codeword")
    

def get_byte_from_arr(arr):
    if(len(arr) != 8):
        raise ValueError("wrong length,should be 8")
        
    byte = 0
    
    for i in range(8):
        byte += arr[i]*(2**(8-(i+1)))
    
    return byte
                     


def predict_erased(input):
    input = np.absolute(input)
    min = np.inf
    min_index= 0
    
    for i in range(3):
        sum = np.sum(input[i:len(input):3])
        if sum < min:
            min = sum
            min_index = i

    return min_index

"""
This function takes a noisy real-valued 1D np.array of size (8*6)k 
It assumes that a third of the coordinates were erased and that there's Gaussian Noise of mean 0 and variance 10
""" 
def prediction(input):
    
    erasedIndex = predict_erased(input)
    input[erasedIndex:len(input):3] = 0
    
    c_0 = np.array([1,1,1,1,1,1])
    c_1 = np.array([-1,-1,-1,-1,-1,-1])
    length = len(c_0)
    
    for i in range(0,input.size,length):
        sub_arr = input[i:i+length]
        
        if np.dot(sub_arr,c_0) >= np.dot(sub_arr,c_1):
            input[i:i+length] = c_0
        else:
            input[i:i+length] = c_1
            
    return input
    
"""
This function takes a 1D np.array of size (8*6)k and returns the string.
It assumes that input is {-1,1}^((8*6)k) with a third of the values being zero
"""
def decode_after_prediction(input):
    output = []
    outer_step = 8*6
    inner_step = 6
    for i in range(0,input.size,outer_step):
        bits = []
        arr = input[i:i+outer_step]
        for j in range(0,arr.size,inner_step):
            bits.append(decode_from_codeword(arr[j:j+inner_step], inner_step))
            
        output.append(get_byte_from_arr(bits))
            
    return str(bytearray(output),'utf-8')

        