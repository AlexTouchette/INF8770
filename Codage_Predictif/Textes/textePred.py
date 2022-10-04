import numpy as np
import matplotlib.pyplot as py


def decode(compressed_text,num_list):
    decode=[]

    #delete first value of compressed_text since it's always the same
    compressed_text.pop(0)
    decode.append(num_list[0])
    for i in range(len(compressed_text)) :
        decode.append(compressed_text[i]+num_list[i])
    return decode

#file_name="Codage_Predictif/textes/ABC.txt"
#file_name="Codage_Predictif/textes/randomText.txt"
file_name="Codage_Predictif/textes/BeeMovieScript.txt"

file = open(file_name)
lines = file.readlines()
print("LEN",len(lines))
num_list=[]
compressed_text=[]
#read text file and change every character to number
for line in lines:
    num_list = [ord(char) for char in line]

fp= open(r'Codage_Predictif/textes/textButNum.txt', 'w')
for num in num_list :
    fp.write(str(num))
#put first number of num_list on compressed_text list since it is unchanged 
compressed_text.append(num_list[0])

#iterate through num and append compressed_text list with prediction error e = xn - xn-1
for i in range(1, len(num_list)):
    error = num_list[i]-num_list[i-1]
    compressed_text.append(error)

print(num_list)
print(compressed_text) 

#write new message in file 
fp= open(r'Codage_Predictif/textes/coded.txt', 'w')
for num in compressed_text :
    fp.write(str(num))


#decompresion to find original text
originalText = decode(compressed_text,num_list)
''' for num in originalText:
    print(chr(num)) '''




#print(chr(65))




