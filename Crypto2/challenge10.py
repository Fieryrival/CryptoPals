import base64
from Crypto.Cipher import AES
# implementation of CBC with AES function in ECB Mode and Xor function
# https://www.educative.io/answers/what-is-cbc

def aes_ecb(input_bytes,key):
    cipher  = AES.new(key,AES.MODE_ECB)
    decrypted_msg = cipher.decrypt(input_bytes)
    return decrypted_msg

def xor_bytes(str1,str2):
    res = b''
    j = 0
    #print(len(str1),len(str2))
    for i in str1:
        res += bytes([i^str2[j]])
        j = j + 1
    return res

def aes_cbc_decrypt(input_bytes,key):
    c0 = b'\x00'*16
    ans = b''
    
    length_of_text = len(input_bytes)
    no_of_blocks = int(length_of_text/16) # here i knew it would be 2880/16 == 180
    for i in range(no_of_blocks):
        c1 = input_bytes[16*i:16*(i+1):]
        aux1 = aes_ecb(c1,key)
        #print(len(c0))
        b1 = xor_bytes(c0,aux1)
        ans += b1
        c0 = c1
    return ans

def main():
    in_file = open('10.txt','rb')
    text = in_file.read()
    decoded_text = base64.b64decode(text)
    #iv_xor = init_vector(decoded_text[:16:])
    key = b'YELLOW SUBMARINE'
    ans = aes_cbc_decrypt(decoded_text,key)
    print(ans.decode('utf-8'))
    in_file.close()

if __name__ == '__main__':
    main()
