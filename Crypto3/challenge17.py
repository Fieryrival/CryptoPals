from random import randint, choices
import string
import base64
from Crypto.Cipher import AES
from os import urandom
# https://robertheaton.com/2013/07/29/padding-oracle-attack/
# https://resources.infosecinstitute.com/topic/padding-oracle-attack-2/
# https://en.wikipedia.org/wiki/Padding_oracle_attack
# https://blog.gdssecurity.com/labs/2010/9/14/automated-padding-oracle-attacks-with-padbuster.html
# https://blog.skullsecurity.org/2013/a-padding-oracle-example


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


def aes_cbc_encrypt(input_bytes, key, iv):
    c0 = iv
    ans = b''
    length_of_text = len(input_bytes)
    no_of_blocks = int(length_of_text/16)
    for i in range(no_of_blocks):
        b1 = input_bytes[16*i:16*(i+1):]
        aux1 = xor_bytes(b1, c0)
        c1 = aes_ecb_encrypt(aux1, key)
        ans += c1
        c0 = c1
    return ans


def aes_cbc_decrypt(input_bytes, key, iv):
    c0 = iv
    ans = b''
    length_of_text = len(input_bytes)
    no_of_blocks = int(length_of_text/16)
    for i in range(no_of_blocks):
        c1 = input_bytes[16*i:16*(i+1):]
        aux1 = aes_ecb_decrypt(c1, key)
        b1 = xor_bytes(aux1, c0)
        ans += b1
        c0 = c1
    return ans


def check_padding(text):
    return text[-1]*text[-1:] == text[-text[-1]:]


def pkcs7_padding(data):  # not mine....copied it ....though quite easy to understand on one look
    pkcs7 = True
    last_byte_padding = data[-1]
    if (last_byte_padding < 1 or last_byte_padding > 16):
        pkcs7 = False
    else:
        for i in range(0, last_byte_padding):
            if (last_byte_padding != data[-1-i]):
                pkcs7 = False
    return pkcs7


def random_aes_key():
    res = ''.join(choices(string.ascii_uppercase +
                  string.ascii_lowercase + string.digits, k=16))
    res = res.encode()
    return res


def pad(input_bytes: bytes, block_size: int) -> bytes:
    padding = block_size - (len(input_bytes) % block_size)
    return input_bytes + bytes([padding]*padding)


def unpad(input_bytes: bytes, block_size: int) -> bytes:
    len = 0
    reversed_bytes = input_bytes[-1]
    return input_bytes[:-input_bytes[-1]]


def fun_one(input_bytes, key, iv):
    padded_bytes = pad(input_bytes, AES.block_size)
    c_text = aes_cbc_encrypt(padded_bytes, key, iv)
    return c_text


def fun_two(input_bytes, key, iv):
    ptext = aes_cbc_decrypt(input_bytes, key, iv)
    validity = check_padding(ptext)
    # print(validity)
    return validity


def padding_oracle_attack(block, key, iv):
    # iv = b'\x00'*16
    res = b''
    suffix = b''
    prev_block = iv
    no_of_blocks = int(len(block)/16)
    k = 0
    while k < no_of_blocks:
        t=0
        x = 0
        while x < 16:
            for i in range(256):
                tmp = iv[:15-t]+bytes([i])+xor_fun(suffix, t+1)
                if fun_two(block[16*k:16*(k+1)], key, tmp) == True:
                    suffix = bytes([i ^ (t+1)]) + suffix
                    t = t + 1
                    break
                    # pass
            x = x+1

        res += xor_bytes(prev_block, suffix)
        prev_block = block[16*k:16*(k+1)]
        suffix = b''
        k = k+1
        t = 0
    res = unpad(res, AES.block_size)
    return res

    pass


def xor_fun(input_bytes, key):
    ans = b''
    for i in input_bytes:
        ans += bytes([i ^ key])
    return ans


def main():
    in_file = open('/home/noob/Documents/Crypto3/17.txt', 'r')
    list_of_text = in_file.readlines()
    text_to_encrypt = list_of_text[randint(0, 9)]
    # text_to_encrypt = list_of_text[5]
    text_to_encrypt = text_to_encrypt.replace("\n", "")
    in_file.close()
    text = base64.b64decode(text_to_encrypt)
    iv = urandom(16)
    # iv = b'\x00'*16  # C1
    key = random_aes_key()
    # print(type(iv))
    enc_msg = fun_one(text, key, iv)
    # print(len(enc_msg))
    # modifed_ctext = input("Enter the text")
    # modifed_ctext = bytes.fromhex(modifed_ctext)
    # plain_text = fun_two(enc_msg, key, iv)
    # tmp = iv[:15]
    suffix = b''
    # ans = b''
    res = b''
    # for k in range(15):
    no_of_blocks = int(len(enc_msg)/16)
    tmp_res = b''
    t = 0
    ans = b''
    # print(2^2)
    x = 0
    i = 0
    p_ = b''

    interm = b''
    # while i < 1:
    #     if i != 0:
    #         iv = enc_msg[16*(i-1):16*(i)]
    #     x = 0
    #     t = 0
    #     suffix = b''
    #     while x < 16:
    #         for k in range(256):
    #             # tmp = iv[:15-t]+bytes([k])+bytes([97 ^ 4]) + \
    #             #     bytes([122 ^ 4])+bytes([121 ^ 4])
    #             tmp = iv[:15-t]+bytes([k])+suffix
    #             if fun_two(enc_msg[16*i:16*(i+1)], key, tmp) == True:
    #                 c1_ = k
    #                 p_1 = aes_cbc_decrypt(enc_msg[16*i:16*(i+1)], key, tmp)
    #                 # p_1 = [t]*t
    #                 p_2 = bytes([t])
    #                 # print((p_1[15-t]),type(k))
    #                 I = c1_ ^ p_1[15-t]
    #                 ptext = I ^ iv[15-t]
    #                 suffix = xor_fun(suffix, t)
    #                 t = t + 1
    #                 suffix = bytes([I]) + suffix
    #                 suffix = xor_fun(suffix, t)
    #                 ans = bytes([ptext])+ans
    #                 # interm = bytes([c1_ ^ p_[15-t]])+interm
    #                 # print(k, I)
    #                 break
    #         x = x+1
    #     suffix = b''
    #     res += ans
    #     ans = b''
    #     interm = b''

    #     i = i+1
    # print(res)
    # print(bytes([5]))
    soluson = padding_oracle_attack(enc_msg, key, iv)
    print(soluson)


if __name__ == '__main__':
    main()
