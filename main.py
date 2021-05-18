# -*- coding: utf-8 -*-
"""
Created on Tue May 18 11:02:04 2021

@author: Harold
"""
import numpy as np




def main():
    input= 'asda@¦#°#@°@§#@#§'
    encoded = encode(input)
    encoded_loss = easyChannel(encoded)
    decoded = decode(encoded_loss)
    print(decoded)
    
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
Takes an input in [0,255] and creates the corresponding 2 times repeated codeword

Example : create_code(1) gives c_1+c_1 where c_1 = (0,1,0,..0) with 255 zeros and only one 1.
"""
def create_code(i):
    arr = np.zeros(256)
    arr[i] = 1
    return np.hstack((arr,arr))

"""
Takes a utf-8 string of length k and outputs the corresponding encoding of length 2k*256 

Example: encode('ab') = c_a+c_a+c_b+c_b 
"""
def encode(input):
    arr = np.array(bytearray(input, 'utf-8')).astype('int')
    output = np.empty
    for i in range(len(arr)):
        output = np.hstack((output,create_code(arr[i])))
        
        #remove empty in the beginning
    return output[1:]

"""
This function takes a 1D np.array of size 2k*256 such that the array represents
2 times repeated codewords of length 256.  
"""
def decode(input):
    output = []
    
    for i in range(0,input.size,512):
        value=np.nonzero(input[i:i+512])[0][0]
        
        if value < 256:
            output.append(value)
        else:
            output.append(value-256)
            
    return str(bytearray(output),'utf-8')
        

"""
WHAT IS BELOW IS NOT INTERESTING BUT KEPT JUST IN CASE
"""


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