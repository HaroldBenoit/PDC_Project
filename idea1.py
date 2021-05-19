# -*- coding: utf-8 -*-
"""
Created on Wed May 19 10:12:11 2021

@author: Harold
"""

import numpy as np


def main():
    code_length = 100
    c_0 = [1 for x in range(code_length)]
    c_1 = [-1 for x in range(code_length)]
    
    codebook = {0:c_0, 1:c_1}
    
    input= '󕘆򋃭񜘽𭡥߂⑌Ю빰OЗ򽰪܏݊扥Ê󣧰󈉊Ο𕐇坲򩒇󜹵񔭕ߒВ~񃚙G񺷩檏T�U␛񥋽񇰦b񴓔ͪ'
    
    encoded = encode(input,codebook)
    encoded_loss = channel(encoded)
    pred = prediction(encoded_loss,codebook)
    decoded = decode_after_prediction(pred,codebook)
    print(decoded)
    print(decoded==input)
    
"""
Noisy channel
"""    
def channel(chanInput):
    chanInput = np.clip(chanInput,-1,1)
    erasedIndex = np.random.randint(3)
    print("ERASED INDEX IS ", erasedIndex)
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
Return the array of bits given a number in [0,255]
"""
def getbits(num):
    bits = []
    for i in range(7,-1,-1):
        bits.append((num >> i)&1)
    return bits

"""
Given a string, transforms into into its binary form and replaces each bit by its corresponding codeword
"""
def encode(input,codebook):
    arr = np.array(bytearray(input, 'utf-8')).astype('int')
    output = np.empty
    for i in range(len(arr)):
        num = arr[i]
        bits = getbits(num)
        for j in range(8):
            codeword = np.array(codebook[bits[j]])
            output = np.hstack((output,codeword))
        
    #remove empty in the beginning
    return output[1:]


"""
GIven a codeword, returns whether it was H=0  or H=1
"""
def decode_from_codeword(arr):
    
    
    for j in range(len(arr)):
        if arr[j] == 1:
            return 0
        elif arr[j] == -1:
            return 1
    
    raise ValueError("array isn't a valid codeword")
    

"""
Given an array of 8 bits, compute the corresponding byte
"""
def get_byte_from_arr(arr):
    if(len(arr) != 8):
        raise ValueError("wrong length,should be 8")
        
    byte = 0
    
    for i in range(8):
        byte += arr[i]*(2**(8-(i+1)))
    
    return byte
                     
"""
predict the erased index 
algo: argmin_{j}{sum over |Yi^2 where i is part of the group (Z/3Z) + j }
"""

def predict_erased(input):
    input = input*input
    min = np.inf
    min_index= 0
    
    for i in range(3):
        sum = np.sum(input[i:len(input):3])
        if sum < min:
            min = sum
            min_index = i

    return min_index

"""
This function does minimum distance-decoding of the given array with the given codebook

"""

def codeword_prediction(arr,codebook):
    min = np.inf
    min_index= 0
    
    for i in range(len(codebook.keys())):
        sub = codebook[i] - arr
        dist = np.dot(sub,sub) ##compute distance
        
        if dist < min:
            min = dist
            min_index = i
            
    return min_index

"""
This function takes a noisy real-valued 1D np.array of size code_length*k, k positive integer
It assumes that a third of the coordinates were erased and that there's Gaussian Noise of mean 0 and variance 10.

It first predicts the erased index and puts every such erased coordinate at 0.

It then does minimum-distance decoding for sub_array of size code_length and replaces it by the found codeword
""" 
def prediction(input, codebook):
    
    erasedIndex = predict_erased(input)
    print("PREDICTED ERASED INDEX IS ", erasedIndex)
    input[erasedIndex:len(input):3] = 0
    
    code_length = len(codebook[0])
    
    for i in range(0,input.size,code_length):
        sub_arr = input[i:i+code_length]
        
        predicted_index = codeword_prediction(sub_arr,codebook)
        input[i:i+code_length] = codebook[predicted_index]
            
    return input
    
"""
This function takes a 1D np.array of size (8*6)k and returns the string.
It assumes that input is {-1,1}^((8*6)k) with a third of the values being zero
"""
def decode_after_prediction(input,codebook):
    output = []
    code_length = len(codebook[0])
    outer_step = 8*code_length
    inner_step = code_length
    
    for i in range(0,input.size,outer_step):
        bits = []
        arr = input[i:i+outer_step]
        for j in range(0,arr.size,inner_step):
            bits.append(decode_from_codeword(arr[j:j+inner_step]))
            
        output.append(get_byte_from_arr(bits))
            
    return str(bytearray(output),'utf-8')


main()