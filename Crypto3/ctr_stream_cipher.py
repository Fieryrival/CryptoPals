import base64
from Crypto.Cipher import AES
from itertools import zip_longest
# took the code straight from https://cedricvanrompay.gitlab.io/cryptopals/challenges/18.html


def aes_ebc_encrypt(ptext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    ctext = cipher.encrypt(ptext)
    return ctext

def bxor(a, b, longest=True):
    if longest:
        return bytes([ x^y for (x, y) in zip_longest(a, b, fillvalue=0)])
    else:
        return bytes([ x^y for (x, y) in zip(a, b)])

def keystream_gen(key, nonce):
    counter = 0
    while True:
        to_encrypt = (nonce.to_bytes(length=8, byteorder='little') +
                      counter.to_bytes(length=8, byteorder='little'))
        keystream_block = aes_ebc_encrypt(to_encrypt, key)
        yield from keystream_block

        counter += 1

def aes_128_ctr(ptext, key, nonce):
    keystream = keystream_gen(key, nonce)

    return bxor(keystream, ptext,longest=False)


def main():
    in_file = open('/home/noob/Documents/Crypto3/18.txt', 'r')
    text = in_file.readline()
    ctext = base64.b64decode(text)
    nonce = 0
    key = b'YELLOW SUBMARINE'
    ptext = aes_128_ctr(ctext,key,nonce)
    print(ptext)
    in_file.close()


if __name__ == '__main__':
    main()
