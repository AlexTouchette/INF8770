import numpy as np
import matplotlib.pyplot as py

# function to decode message 
def decode(compressed_text,num_list):
    
    decode=[]

    #delete first value of compressed_text since it's always the same
    compressed_text.pop(0)

    decode.append(num_list[0])
    for i in range(len(compressed_text)) :
        decode.append(compressed_text[i]+num_list[i])
    
    return decode



# path to deferent txt files

#file_name="Codage_Predictif/textes/ABC.txt"
#file_name="Codage_Predictif/textes/randomText.txt"
fileName="Codage_Predictif/textes/BeeMovieScript.txt"
compressedText=[]


# open file  and store it's different lines in a list
file = open(fileName)
lines = file.readlines()


# read text file and change every character to number
for line in lines:
    numList = [ord(char) for char in line]


# create a file with containing the original text but converted to number
# this will help us compare file sizes before and after compression 
fp= open(r'Codage_Predictif/textes/TextNum.txt', 'w')
for num in numList :
    fp.write(str(num))


# put first number of num_list on compressed_text list since it is unchanged 
compressedText.append(numList[0])

# iterate through num and append compressed_text list with prediction error e = Xn - X̂n 
# here X̂n = xn−1
for i in range(1, len(numList)):
    error = numList[i]-numList[i-1]
    compressedText.append(error)

print("ORIGINAL TEXT (numbers)",numList)
print("ORIGINAL TEXT AFTER COMPRESSION",compressedText)

# write compressed message in file
# this will help us compare file sizes before and after compression 
fp= open(r'Codage_Predictif/textes/compressedText.txt', 'w')
for num in compressedText :
    fp.write(str(num))


# decode compressed message to find original text
originalText = decode(compressedText,numList)
print("ORIGINAL TEXT AFTER COMPRESSION",originalText)





