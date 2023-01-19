from Crypto.Cipher import AES
from os import urandom
import base64
from Crypto.Util.Padding import pad, unpad


def aes_ecb_encrypt(input_bytes, key):
    input_bytes = pad(input_bytes, AES.block_size)
    cipher = AES.new(key, AES.MODE_ECB)
    ctext = cipher.encrypt(input_bytes)
    return ctext


def aes_ecb_decrypt(input_bytes, key):
    decipher = AES.new(key, AES.MODE_ECB)
    ptext = decipher.decrypt(input_bytes)
    return ptext


def counter(n):
    # n=n-1
    index = int(n / 256)
    remainder = n % 256
    ans = b''
    if remainder != 0:
        ans = (bytes([255])*index)+bytes([remainder])
    else:
        ans = (bytes([255])*index)+bytes([index])
    ans += b'\x00'*(8-len(ans))
    return ans


def xor_str(str1, str2):
    min_val = min(len(str1), len(str2))
    res = b''
    # if min_val != 16:
    #     return str1
    for i in range(min_val):
        tmp_val = str1[i] ^ str2[i]
        res += bytes([tmp_val])
    return res


def ctr_encrypt(ptext, key, nonce):
    blocks = int(len(ptext)/16)
    ctext = b''
    for i in range(blocks):
        tmp_ptext = ptext[16*i:16*(i+1)]
        keystream = key_stream(nonce, i)
        aux = aes_ecb_encrypt(keystream, key)
        ctext += xor_str(tmp_ptext, aux)
    # ctext += ptext[16*blocks:]
    return ctext


def ctr_decrypt(ctext, key, nonce):
    blocks = int(len(ctext)/16)
    ptext = b''
    for i in range(blocks):
        tmp_ctext = ctext[16*i:16*(i+1)]
        keystream = key_stream(nonce, i)
        aux = aes_ecb_encrypt(keystream, key)
        ptext += xor_str(tmp_ctext, aux)
    # ptext += ctext[16*blocks:]
    return ptext


def key_stream(nonce_part, n):
    countr = counter(n)
    key_str = nonce_part + countr
    return key_str


def main():
    in_file = open('/home/noob/Documents/Crypto3/18.txt', 'rb')
    text = in_file.read()
    ciphertext = base64.b64decode(text)
    # print(ciphertext)
    in_file.close()
    # key = urandom(16)
    key = b'YELLOW SUBMARINE'
    nonce = b'\x00'*8
    # test = b'A'*16
    # ctext = ctr_encrypt(test, key, nonce)
    # print(ctext)
    ptext = ctr_decrypt(ciphertext, key, nonce)
    print(ptext, len(ptext))


if __name__ == '__main__':
    main()
