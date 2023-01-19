import random
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import string
import base64
from os import urandom
import random


def encryption_oracle(input_bytes):
    len_of_text = int(len(input_bytes)/32)
    for i in range(len_of_text):
        for j in range(i+1, len_of_text):
            str1 = input_bytes[i*32:(i+1)*32:]
            str2 = input_bytes[j*32:(j+1)*32:]
            if str1 == str2:
                return 'ECB'
    return 'CBC'


def aes_ecb_encrypt(input_bytes, key):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_msg = cipher.encrypt(input_bytes)
    return encrypted_msg


def random_aes_key():
    res = ''.join(random.choices(string.ascii_uppercase +
                  string.ascii_lowercase + string.digits, k=16))
    return res


def unpad(input_bytes: bytes, block_size: int) -> bytes:
    len = 0
    # reversed_bytes = input_bytes[-1]
    return input_bytes[:-input_bytes[-1]]


def decrypt_fun(input_bytes, key, random_str, index):
    n = 0
    prefix = b''
    block = 0
    tmp_res = b''
    flag = 0
    while n < 16 and block < int(len(input_bytes)/16):
        if flag == 0 and (index - n) >= 1:
            my_data = random_str + b'A'*(index-n-1)+tmp_res
            # sample_data = my_data+input_bytes[(16*block)+n:]+b'A'*(n+1)
            if block == 1:
                flag = 1
        else:
            # my_data = b"Rollin' in my 5." + b'A'*(16-n-1) + tmp_res
            my_data = prefix + b'A'*(16-n-1)+tmp_res
        sample_data = my_data+input_bytes[(16*block)+n:]+b'A'*(n+1)
        for j in range(256):
            lol = my_data+bytes([j])
            tmp_enc = aes_ecb_encrypt(lol, key)
            target_enc = aes_ecb_encrypt(sample_data, key)
            if tmp_enc[16*block:16*(block+1)] == target_enc[16*block:16*(block+1)]:
                tmp_res += bytes([j])
                n = n + 1
                if n == 16:
                    prefix += tmp_res
                    tmp_res = b''
                    block = block + 1
                    n = 0
        # print(tmp_res) # can comment this code for a better view of the working of above block
    return prefix


def AES_128_ECB():
    prefix_str = ''.join(random.choices(string.ascii_uppercase +
                         string.ascii_lowercase+string.digits, k=(random.randint(5, 10))))
    return prefix_str


def extra_block_size(input_bytes, key, prefix):
    sz = 0
    block_sz = 0
    my_str_len = 0
    flag = 0
    for i in range(1, 20):
        tmp = b'A'*i
        data1 = prefix + tmp + input_bytes
        data1 = pad(data1, AES.block_size)
        enc1 = aes_ecb_encrypt(data1, key)
        tmp = b'A'*(i+1)
        data2 = prefix + tmp + input_bytes
        data2 = pad(data2, AES.block_size)
        enc2 = aes_ecb_encrypt(data2, key)
        if enc1[:16] == enc2[:16]:
            # my_str_len = i
            # flag = 1
            return i
        # print(len(enc1), len(enc2))

    return 0


def main():
    res = random_aes_key()
    res = res.encode()
    key = res
    add_str = b'''Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK'''
    # add_str = add_str.decode('utf-8')
    decoded_str = base64.b64decode(add_str)
    # padded the original string to block size
    padded_str = pad(decoded_str, AES.block_size)
    # answer = decrypt_fun(padded_str, key)
    # output = unpad(answer, 16)
    # output = output.decode('utf-8')
    # print(output)
    prefix = AES_128_ECB()
    prefix = prefix.encode()
    # print(len(prefix), prefix)
    index = extra_block_size(decoded_str, key, prefix)
    # print(index)
    # after reading some hints and explainations i need to know the size of random string and then the length to append for first block
    ans = decrypt_fun(padded_str, key, prefix, index)
    # print(ans)
    ans = unpad(ans, AES.block_size)
    ans = ans.decode('utf-8')
    print(ans)


if __name__ == '__main__':
    main()
