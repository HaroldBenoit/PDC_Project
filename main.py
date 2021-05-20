# -*- coding: utf-8 -*-
"""
Created on Wed May 19 22:38:45 2021

@author: Harold
"""
"""
Created on Wed May 19 10:12:11 2021

@author: Harold
"""

import numpy as np


def main():
    code_length = 150
    # k is the number of bits sent per codeword, is a power of 2
    k=1
    
    # here we define the coodebook. The cardinality of the codebook is k.
    codebook = create_codebook(code_length)
    
    ## here we define the decoding function specific to our codebook
    decoding_function = decode_codebook
    
    ## defining the input text
    input= '¦@@@@#°§¬|¢¢9+"*ç%&/()'
    
    ## This part is the encoding->channel->prediction->decoding loop
    
    ## One should be able to define k, codebook and decoding_function without changing
    ## the code below. It's modular baby
    
    encoded = encode(input,codebook,k)
    encoded_loss = channel(encoded)
    pred = prediction(encoded_loss,codebook)
    
    decoded = decode_after_prediction(pred,codebook,k,decoding_function)
    print(decoded)
    print(decoded==input)
    
    
    
def create_codebook(code_length):
    c_0 = [1 for x in range(code_length)]
    c_1 = [-1 for x in range(code_length)]
    
    codebook = {0:c_0, 1:c_1}
    
    return codebook


"""
Given a codeword, returns the corresponding mapping
"""
def decode_codebook(arr):
    for j in range(len(arr)):
        if arr[j] == 1:
            return 0
        elif arr[j] == -1:
            return 1
    
    raise ValueError("array isn't a valid codeword")
        

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
Return the array of tuples of bits of size k given a number in [0,255]
"""
def getbits(num,k):
    bits = []
    mask = 255 >> (8-k)
    for i in range(8-k,-1,-k):
        bits.append((num >> i)&mask)
    return bits

"""
Given a string, transforms into into its binary form and replaces each bit by its corresponding codeword
"""
def encode(input,codebook,k):
    arr = np.array(bytearray(input, 'utf-8')).astype('int')
    output = np.empty
    for i in range(len(arr)):
        num = arr[i]
        bits = getbits(num,k)
        for j in range(8//k):
            codeword = np.array(codebook[bits[j]])
            output = np.hstack((output,codeword))
        
    #remove empty in the beginning
    return output[1:]




"""
Given an array of tuples of k bits, compute the corresponding byte
"""
def get_byte_from_arr(arr,k):
    
    string = "{0:0" +str(k)+"b}"
    buff = ''
    
    for i in range(len(arr)):
        buff = buff + string.format(arr[i])
    
    return int(buff,2)
                     
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
This function counts the number of coordinates above zero and below zero and
ouputs on the majority (i.e. there are more coordinates < 0 -> we output 1 else 0)

"""

def codeword_prediction(arr,codebook):
    count0 = 0
    count1 = 0
    
    for i in range(arr.size):
        num = arr[i]
        if num < 0:
            count1 += 1
        elif num > 0:
            count0 += 1
    
            
    return 0 if count0 >= count1 else 1

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
This function takes a 1D np.array representing the encoded binary string and returns the string. 
"""
def decode_after_prediction(input,codebook,k,decoding_function):
    output = []
    code_length = len(codebook[0])
    outer_step = 8*code_length
    inner_step = k*code_length
    
    for i in range(0,input.size,outer_step):
        bits = []
        arr = input[i:i+outer_step]
        for j in range(0,arr.size,inner_step):
            bits.append(decoding_function(arr[j:j+inner_step]))
            
        output.append(get_byte_from_arr(bits,k))
            
    return str(bytearray(output),'utf-8')


main()