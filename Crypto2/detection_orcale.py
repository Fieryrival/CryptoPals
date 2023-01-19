# in this challenge we need to create functions to first encrypt with either ecb or cbc mode then detect what mode is being used

import random
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import string
import base64
from os import urandom
import random


def ecb_cbc_detector(input_bytes):
    len_of_text = int(len(input_bytes)/32)
    for i in range(len_of_text):
        for j in range(i+1, len_of_text):
            str1 = input_bytes[i*32:(i+1)*32:]
            str2 = input_bytes[j*32:(j+1)*32:]
            if str1 == str2:
                return 'ECB'
    return 'CBC'


def aes_cbc_decrypt(input_bytes, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct_bytes = cipher.decrypt(input_bytes)
    decrypted_msg = ct_bytes
    return decrypted_msg


def aes_ecb_encrypt(input_bytes, key):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_msg = cipher.encrypt(pad(input_bytes, AES.block_size))
    return encrypted_msg


def aes_cbc_encrypt(input_bytes, key):
    cipher = AES.new(key, AES.MODE_CBC)
    # if iv != b'':
    #    cipher.iv = iv
    ct_bytes = cipher.encrypt(pad(input_bytes, AES.block_size))
    encrypted_msg = ct_bytes  # ciphertext_bytes
    return {'encrypted_msg': ct_bytes, 'iv': cipher.iv}


def random_encrypt(input_bytes, key):
    # key = urandom(16)
    padded = urandom(random.randint(5, 10))+input_bytes + \
        urandom(random.randint(5, 10))
    x = random.randint(0, 1)
    # iv = b''
    print("x=" + str(x))
    if x == 1:
        return aes_ecb_encrypt(padded, key)
    else:
        return aes_cbc_encrypt(padded, key)['encrypted_msg']


def random_aes_key():
    res = ''.join(random.choices(string.ascii_uppercase +
                  string.ascii_lowercase + string.digits, k=16))
    return res


def main():

    res = random_aes_key()
    res = res.encode()
    # print(res)
    # in_file = open("/home/noob/Documents/Crypto2/10.txt","rb")
    # test = in_file.read()
    # data = base64.b64decode(test)
    for i in range(30, 50):
        data = b"A"*i
        key = b"YELLOW SUBMARINE"
        # iv = b'\x00'*16
        # iv = b''
        ans = random_encrypt(data, res)
        print(ans)
        encoded_ans = ans.hex()
        detection_rezult = ecb_cbc_detector(encoded_ans)
        print(detection_rezult)
    # in_file.close()

    # in_file = open("/home/noob/Documents/Crypto1/challenge8/8.txt", "rb")
    # test = in_file.readlines()
    # j = 0
    # for k in test:
    #    j = j + 1
    #    if ecb_cbc_detector(k) == 'ECB':
    #        print(j)
        # print(ecb_cbc_detector(k))
    # in_file.close()


if __name__ == '__main__':
    main()
