#taken help from https://0xss0rz.github.io/2019-08-23-Cryptopals-Write-Ups/
# https://laconicwolf.com/2018/05/29/cryptopals-challenge-3-single-byte-xor-cipher-in-python/

def single_byte_xor(input_bytes,single_char):
    ans = b''
    for i in input_bytes:
        ans = ans + bytes([i^single_char])
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
        sum = sum + character_frequencies.get(chr(i),0)
    return sum
def main():
    encoded_string = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    # encoded_string = '73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d'
    decoded_hex_text = bytes.fromhex(encoded_string)
    possible_ans = []
    #print(decoded_hex_text)
    for i in range(256):
        xorred = single_byte_xor(decoded_hex_text,i)
        #print(xorred)
        score = get_english_score(xorred)
        data = {
            'message' : xorred,
            'score': score,
            'key': i
            }
        possible_ans.append(data)
        #print(f'{i} : {xorred} : {score}')
    sorted_dict = sorted(possible_ans,key = lambda x:x['score'],reverse=True)
    print(sorted_dict[0])
    
if __name__ == '__main__':
    main()