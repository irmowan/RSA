__author__ = 'irmo'
import re

IP = [
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7,
    56, 48, 40, 32, 24, 16, 8, 0,
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6]
IP_inverse = [
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25,
    32, 0, 40, 8, 48, 16, 56, 24]
E = [
    31, 0, 1, 2, 3, 4,
    3, 4, 5, 6, 7, 8,
    7, 8, 9, 10, 11, 12,
    11, 12, 13, 14, 15, 16,
    15, 16, 17, 18, 19, 20,
    19, 20, 21, 22, 23, 24,
    23, 24, 25, 26, 27, 28,
    27, 28, 29, 30, 31, 0]

Sbox = [
    # S0
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
     0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
     4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
     15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

    # S1
    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
     3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
     0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
     13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

    # S2
    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
     13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
     13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
     1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

    # S3
    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
     13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
     10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
     3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

    # S4
    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
     14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
     4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
     11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

    # S5
    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
     10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
     9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
     4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

    # S6
    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
     13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
     1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
     6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

    # S7
    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
     1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
     7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
     2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
]

P = [
    15, 6, 19, 20, 28, 11, 27, 16,
    0, 14, 22, 25, 4, 17, 30, 9,
    1, 7, 23, 13, 31, 26, 2, 8,
    18, 12, 29, 5, 21, 10, 3, 24]

Round_Left = [
    1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# Permuted Choice
PC1 = [
    # Left C
    56, 48, 40, 32, 24, 16, 8,
    0, 57, 49, 41, 33, 25, 17,
    9, 1, 58, 50, 42, 34, 26,
    18, 10, 2, 59, 51, 43, 35,
    # Right D
    62, 54, 46, 38, 30, 22, 14,
    6, 61, 53, 45, 37, 29, 21,
    13, 5, 60, 52, 44, 36, 28,
    20, 12, 4, 27, 19, 11, 3]

PC2 = [
    13, 16, 10, 23, 0, 4,
    2, 27, 14, 5, 20, 9,
    22, 18, 11, 3, 25, 7,
    15, 6, 26, 19, 12, 1,
    40, 51, 30, 36, 46, 54,
    29, 39, 50, 44, 32, 47,
    43, 48, 38, 55, 33, 52,
    45, 41, 49, 35, 28, 31]

global CIRCLE
CIRCLE = 6


# Above is constants
# Below is functions

def list2string(l):
    s = ''
    for i in range(len(l)):
        s += str(l[i])
    return s


def string2list(s):
    l = [int(x) for x in s]
    return l


def s_box(sbox_in):
    sbox_out = []
    for i in range(8):
        box_in = sbox_in[6 * i:6 * i + 6]
        row = box_in[0] * 2 + box_in[5]
        column = box_in[1] * 8 + box_in[2] * 4 + box_in[3] * 2 + box_in[4]
        num = Sbox[i][row * 16 + column]
        bin_num = '{0:04b}'.format(num)
        box_out = [int(bin_num[x]) for x in range(4)]
        sbox_out += box_out
    return sbox_out


def f(R, K):
    R_EP = [R[x] for x in E]
    sbox_in = list_xor(R_EP, K)
    sbox_out = s_box(sbox_in)
    P_EP = [sbox_out[x] for x in P]
    return P_EP


def list_xor(x, y):
    return [(a[0] ^ a[1]) for a in list(zip(x, y))]


# Return a list of subkeys
def generating_key(Key):
    C = []
    D = []
    K = []
    C.append([Key[x] for x in PC1[0:28]])
    D.append([Key[x] for x in PC1[28:56]])
    # Generating subkeys
    for i in range(16):
        move = Round_Left[i]
        C.append(C[-1][move:] + C[-1][:move])
        D.append(D[-1][move:] + D[-1][:move])
        CD = C[-1] + D[-1]
        K.append([CD[x] for x in PC2])
    return K


# Type decides encrypt or decrypt
# Key will be used to generate subkeys
# Default type is encrypting
def DES(Message, Key, Type=1):
    L = []
    R = []
    K = generating_key(Key)
    L.append([Message[x] for x in IP[0:32]])
    R.append([Message[x] for x in IP[32:64]])
    # Here it should run CIRCLE times
    if Type == 1:
        for i in range(CIRCLE):
            L.append(R[i])
            R.append(list_xor(L[i], f(R[i], K[i])))
        LR = R[-1][:] + L[-1][:]
        result = [LR[x] for x in IP_inverse]
    else:
        for i in range(CIRCLE):
            L.append(R[i])
            R.append(list_xor(L[i], f(R[i], K[CIRCLE - i - 1])))
        LR = R[-1][:] + L[-1][:]
        result = [LR[x] for x in IP_inverse]
    # Change a list to string
    return list2string(result)


# Padding a message
def padding(Message):
    num_padding = int(8 - (len(Message) % 64) / 8)
    for i in range(num_padding):
        s_padding = '{0:08b}'.format(num_padding)
        for j in range(8):
            Message.append(int(s_padding[j]))
    return Message


def unpadding(result):
    s = result;
    num_padding = int(result[-8:], 2)
    flag = 1
    if num_padding <= 0 or num_padding > 8:
        print("Padding is incorrect")
    for i in range(1, num_padding):
        if int(result[-8 * i - 8:-8 * i], 2) != num_padding:
            flag = 0
    if flag == 1:
        s = result[:-8 * num_padding]
    return s


def legality(Key, IV, Message):
    if len(Key) != 64:
        print('The length of Key should be 64 bits, please check it and input again.')
        return 0
    if len(IV) != 64:
        print('The length of IV should be 64 bits, please check it and input again.')
        return 0
    if re.match('[01]*[^01]', Key) == 1:
        print('The input Key is not a 01 string.')
        return 0
    if re.match('[01]*[^01]', IV) == 1:
        print('The input IV is not a 01 string.')
        return 0
    if re.match('[01]*[^01]', Message) == 1:
        print('The input text is not a 01 string.')
        return 0
    return 1


def generating_IV():
    import random
    s = ''
    for i in range(64):
        s += str(random.randint(0, 1))
    return s


def main():
    print('Hello, DES!')

    # Choose a type
    print('1. Encrypt a plain text')
    print('2. Decrypt a cipher text')
    print('Enter the choice(1 or 2):')
    choice = int(input())

    # Read input from files
    file_Key = open('Key.txt', 'r')
    file_Text = open('Text.txt', 'r')
    IV = generating_IV()
    Key = file_Key.read().strip()
    Message = file_Text.read().strip()

    print('IV:     ', IV)
    print('Key:    ', Key)
    print('Text:   ', Message)
    print()

    # Check legality of input
    if legality(Key, IV, Message) == 0:
        return

    IV = string2list(IV)
    Key = string2list(Key)
    Message = string2list(Message)
    if choice == 1:
        # Check input
        if (len(Message) % 8 != 0) or (len(Message) == 0):
            print('The length of plain text must be multiple of 8, and could not be 0.')
            return
        Message = padding(Message)

        # Encrypt a plain text
        print('Encrypt plain text:')
        cipher = ''
        cipher += DES(IV, Key)
        for i in range(int(len(Message) / 64)):
            m = Message[64 * i:64 * i + 64]
            last_cipher = cipher[-64:]
            last_cipher_list = [int(last_cipher[x]) for x in range(64)]
            cipher += DES(list_xor(m, last_cipher_list), Key)
        print('Result: ', cipher)
    else:
        # Check input
        if (len(Message) % 64 != 0) or (len(Message) < 128):
            print('The length of cipher text must be multiple of 64, and at least 128.')
            return

        # Decrypt a cipher text
        print('Decrypt cipher text:')
        result = ''
        IV = ''
        for i in range(int(len(Message) / 64)):
            m = Message[64 * i:64 * i + 64]
            if i == 0:
                IV = DES(m, Key, 2)
            else:
                result_temp = [int(x) for x in DES(m, Key, 2)]
                last_text = Message[64 * i - 64:64 * i]
                result += list2string(list_xor(result_temp, last_text))
        result = unpadding(result)
        print('Result: ', result)
    return


main()
