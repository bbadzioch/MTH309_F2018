from sympy import *
import numpy as np
import string
from pathlib import Path


supp_folder = Path("supplements")
text_file =  supp_folder/"aphorisms.txt"


def show_encoding():
    alphabet = '_' + string.ascii_uppercase
    for c in alphabet:
        print("{:>3}".format(c), end='')
    print('')
    for n in range(len(alphabet)):
        print("{:>3}".format(n), end='')

   
    
def num2char(numlist):
    N = 20
    chars = []
    for i, n in enumerate(numlist):
        n = int(n)
        print("{:>4}".format(n), end = ''),
        if n == 0: 
            chars.append('_')
        elif n < 0 or n > 26:
            chars.append("\N{FULL BLOCK}")
        else:
            chars.append(chr(n+64))
        if (i+1)%N == 0 or i == len(numlist)-1:
            print('')
            for c in chars:
                print("{:>4}".format(c), end = ''),
            print('\n')
            chars = []



def char2num(s):
    numlist = []
    S = s.upper()
    for c in S:
        if c in string.ascii_uppercase:
            numlist.append(ord(c) - ord('A') + 1)
        elif c == ' ':
            numlist.append(0)
        else:
            numlist.append(99)
    return numlist



def choose_key():
    d = 0 
    while d not in  [1, -1]:
        A = Matrix(np.random.randint(0, 4, (3,3)))
        d = A.det()
    return A, A.inv()


def make_cipher(s=None):
    global text_file
    
    with open(text_file, 'r') as foo:
        lines = foo.readlines()
    text = 'CLASSIFIED ' + np.random.choice(lines).strip()
    text = text + ' '*(((-1)*len(text))%3)
    nums = Matrix(char2num(text)).reshape(len(text)//3, 3).T
    A, AI = choose_key()
    cipher = [int(x) for x in list((A*nums).T)]
    if s == 'show_all':
        return cipher, text, A, AI
    else:
        return cipher


def hill_decoder(K, cipher):
    m =  Matrix(cipher).reshape(len(cipher)//3, 3).T
    return num2char([int(x) for x in list((K*m).T)])

