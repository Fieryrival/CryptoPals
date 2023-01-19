import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from os import urandom
from random import randint, choices
import string
# implementation of CBC with AES function in ECB Mode and Xor function
# https://www.educative.io/answers/what-is-cbc
# https://resources.infosecinstitute.com/topic/cbc-byte-flipping-attack-101-approach/


def cbc_encrypt(input_bytes, key):
    cipher = AES.new(key, AES.MODE_CBC, b'\x00'*16)
    enc_msg = cipher.encrypt(input_bytes)
    return enc_msg


def aes_ecb_encrypt(input_bytes, key):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_msg = cipher.encrypt(input_bytes)
    return encrypted_msg


def aes_ecb_decrypt(input_bytes, key):
    decipher = AES.new(key, AES.MODE_ECB)
    decrypted_msg = decipher.decrypt(input_bytes)
    return decrypted_msg


def xor_bytes(str1, str2):
    res = b''
    j = 0
    # print(len(str1),len(str2))
    for i in str1:
        res += bytes([i ^ str2[j]])
        j = j + 1
    return res


def aes_cbc_encrypt(input_bytes, key):
    c0 = b'\x00'*16
    ans = b''
    length_of_text = len(input_bytes)
    no_of_blocks = int(length_of_text/16)
    for i in range(no_of_blocks):
        c1 = input_bytes[16*i:16*(i+1):]
        aux1 = xor_bytes(c0, c1)
        b1 = aes_ecb_encrypt(aux1, key)
        ans += b1
        c0 = b1
    return ans


def aes_cbc_decrypt(input_bytes, key):
    c0 = b'\x00'*16
    ans = b''
    length_of_text = len(input_bytes)
    no_of_blocks = int(length_of_text/16)
    for i in range(no_of_blocks):
        c1 = input_bytes[16*i:16*(i+1):]
        aux1 = aes_ecb_decrypt(c1, key)
        b1 = xor_bytes(c0, aux1)
        ans += b1
        c0 = c1
    return ans


def cbc_fun_one(key):
    arbitrary_input = "comment1=cooking%20MCs;userdata="
    arbitrary_input = arbitrary_input.encode()
    str_to_append = ''';comment2=%20like%20a%20pound%20of%20bacon'''
    str_to_append = str_to_append.encode()
    input_str = input('Enter your input string=')
    input_str = input_str.replace('=', '')
    input_str = input_str.replace(';', '')
    input_str = input_str.encode()
    input_str = pad(input_str,AES.block_size)
    final_str = arbitrary_input+input_str+str_to_append
    final_str = pad(final_str, AES.block_size)
    # print(final_str)
    # result = dict(pair.split('=') for pair in decoded.split('&'))
    enc_msg = aes_cbc_encrypt(final_str, key)
    return [enc_msg,final_str]


def cbc_fun_two(enc_msg, key):
    res = aes_cbc_decrypt(enc_msg, key)
    print(res)
    # res = res.decode()
    # print(res)
    result = tuple(pair.split(b'=') for pair in res.split(b';'))
    return result


def random_aes_key():
    res = ''.join(choices(string.ascii_uppercase +
                  string.ascii_lowercase + string.digits, k=16))
    return res

def payload(enc_msg,plaintext_input):
    s1 = plaintext_input
    s2 = bytes.fromhex(enc_msg)
    modify_str = b';admin=true;'
    payload_data = ''
    for i in range(len(modify_str)):
        lol = (modify_str[i]^s1[49+i]^s2[33+i]) #s2[34:36]
        lol = hex(lol)
        lol = (lol[2:])
        payload_data+=lol
    tmp_ans = enc_msg[:66]+payload_data+ enc_msg[66+len(payload_data):]
    # print(tmp_ans)
    # tmp_ans = tmp_ans.encode()
    return tmp_ans
    
    

def main():
    key = random_aes_key()
    key = key.encode()
    fun_one_data = cbc_fun_one(key)
    enc = fun_one_data[0]
    sample_text = fun_one_data[1]
    enc_hex = enc.hex()
    # attacker_input = input('Enter attacked ciphertext=')
    attacker_input = payload(enc_hex,sample_text)
    attacker_input = bytes.fromhex(attacker_input)
    # print(attacker_input)
    decrypted = cbc_fun_two(attacker_input, key)
    print(decrypted)
    if [b'admin',b'true'] in decrypted:
        print("Attack Successful!!")


if __name__ == '__main__':
    main()
