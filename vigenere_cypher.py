import nltk
from nltk.corpus import stopwords
import string
import numpy as np
import random
import math
import re

n = 26
alphabet = "abcdefghijklmnopqrstuvwxyz"
spec_chars = string.punctuation +'“'+'”'+'-'+'’'+'‘'+'—' + " " + "1234567890"
friedman_index = 0.0644

def main():
    with open('TheCatcherInTheRye.txt', encoding='utf-8', newline='') as file:
        str = file.read(10000).lower()
    key = get_random_seed(5)

    print('Шифруется случайным ключом:')
    print(key)
    cypher_text = encode(key,str)
    
    print('Зашифрованный текст:')
    print(cypher_text[0:1000])
    
    print('Расшифрованный текст:')
    print(friedman(cypher_text)[0:1000])

def encode(key, plain_text):
    text_length = len(plain_text)
    cypher_text=""
    g = 0
    for i in range(0,text_length):
        if (96<ord(plain_text[i])<123):
            t = ((ord(plain_text[i]) - 97) + (ord(key[g % len(key)]) - 97)) % 26
            cypher_text = cypher_text+alphabet[t]
            g += 1
        else:
            cypher_text = cypher_text+plain_text[i]
    return cypher_text

def decode(key, cypher_text):
    text_length = len(cypher_text)
    plain_text=""
    g = 0
    for i in range(0,text_length):
        if (96<ord(cypher_text[i])<123):
            t = ((ord(cypher_text[i]) - 97) - (ord(key[g % len(key)]) - 97))  % 26
            plain_text = plain_text+alphabet[t]
            g += 1
        else:
            plain_text = plain_text+cypher_text[i]
    return plain_text

def friedman(cypher_text):
    # поиск длины ключа
    temp_text = "".join([ch for ch in cypher_text if 96<ord(ch)<123])
    ind_norm = np.array([])
    for i in range(2,10):
        indexes = np.array([])
        for j in range(0,i):
            temp_text_2 = temp_text[j::i]
            indexes = np.append(indexes, calculate_friedman_index(temp_text_2))
        ind_norm = np.append(ind_norm, np.linalg.norm(indexes-friedman_index))
    length = np.argmin(ind_norm)+2

    columns = []
    for j in range(0,length):
        columns.append(temp_text[j::length])

    mutual_indexes = dict()
    for i in range(0,length-1):
        for j in range(i+1, length):
            t = 0
            sh = 0
            for s in range(0,26):
                temp = calculate_mutual_index(columns[i],shift(columns[j],s))
                if temp > t:
                    t = temp
                    sh = s
            mutual_indexes[(i,j)]=(t,sh)

    d = dict()
    for i in range(0,26):
        dif_temp = abs(calculate_friedman_index(shift(columns[0],i)) - friedman_index)
        d[i]=dif_temp
    sorted_keys = sorted(d, key=d.get)

    keys=[alphabet[it] + "".join([alphabet[(it+mutual_indexes[(0,j)][1])%26] for j in range(1,length)]) for it in sorted_keys]

    stop_words = list(stopwords.words('english'))[0:50]

    occ = 0
    result_key = ""
    for key in keys:
        text2 = decode(key,temp_text)
        occ_temp =  sum([text2.count(word) for word in stop_words])
        if occ_temp > occ:
            occ = occ_temp
            result_key = key

    return decode(result_key, cypher_text)

def shift(text,k):
    result = "".join([alphabet[(ord(ch)-97-k)%26] for ch in text])
    return result

def calculate_friedman_index(text):
    friedman_index = 0
    l = len(text)
    for i in range(0, len(alphabet)):
        t = text.count(alphabet[i])
        friedman_index += (t*(t-1))/(l*(l-1))
    return friedman_index

def calculate_mutual_index(text1,text2):
    mutual_index = 0
    temp_text1 = "".join([ch for ch in text1 if 96<ord(ch)<123])
    temp_text2 = "".join([ch for ch in text2 if 96<ord(ch)<123])
    l1 = len(temp_text1)
    l2 = len(temp_text2)
    for i in range(0, len(alphabet)):
        t1 = temp_text1.count(alphabet[i])
        t2 = temp_text2.count(alphabet[i])
        mutual_index += (t1*t2)/(l1*l2)
    return mutual_index

def get_random_seed(length):
    seed = ""
    for i in range(0,length):
        a = random.randint(0,25)
        seed = seed + alphabet[a]
    return seed

if __name__ == '__main__':
   main()
