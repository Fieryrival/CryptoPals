import base64
from os import urandom
from Crypto.Cipher import AES
from itertools import zip_longest

# didnt understand as what to do in this so looked up a few tutorials


def single_byte_xor(input_bytes, single_char):
    ans = b''
    for i in input_bytes:
        ans = ans + bytes([i ^ single_char])
    return ans


def get_english_score(input_bytes):
    character_frequencies = {
        'a': .08167, 'b': .01492, 'c': .02782, 'd': .04253,
        'e': .12702, 'f': .02228, 'g': .02015, 'h': .06094,
        'i': .06094, 'j': .00153, 'k': .00772, 'l': .04025,
        'm': .02406, 'n': .06749, 'o': .07507, 'p': .01929,
        'q': .00095, 'r': .05987, 's': .06327, 't': .09056,
        'u': .02758, 'v': .00978, 'w': .02360, 'x': .00150,
        'y': .01974, 'z': .00074, ' ': .13000
    }
    sum = 0
    for i in input_bytes.lower():
        sum = sum + character_frequencies.get(chr(i), 0)
    return sum


def aes_ebc_encrypt(ptext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    ctext = cipher.encrypt(ptext)
    return ctext


def bxor(a, b, longest=True):
    if longest:
        return bytes([x ^ y for (x, y) in zip_longest(a, b, fillvalue=0)])
    else:
        return bytes([x ^ y for (x, y) in zip(a, b)])


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

    return bxor(keystream, ptext, longest=False)


def single_byte_xor_attack(text):
    possible_ans = []
    for i in range(256):
        xorred = single_byte_xor(text, i)
        score = get_english_score(xorred)
        data = {
            'message': xorred,
            'score': score,
            'key': i
        }
        possible_ans.append(data)
    sorted_dict = sorted(possible_ans, key=lambda x: x['score'], reverse=True)
    return sorted_dict[0]
    pass


def main():
    in_file = open('/home/noob/Documents/Crypto3/20.txt', 'r')
    list_of_text = in_file.readlines()
    in_file.close()
    ptexts = []
    for i in list_of_text:
        ptexts.append(base64.b64decode(i))
    # print(len(ptexts))
    ctexts = []
    nonce = 0
    key = urandom(16)
    for i in ptexts:
        ctexts.append(aes_128_ctr(i, key, nonce))

    columns = [single_byte_xor_attack(l)['message'] for l in zip(*ctexts)]
    for msg in zip(*columns):
        print(bytes(msg).decode())
    


if __name__ == '__main__':
    main()
