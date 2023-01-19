import base64

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

def to_binary(input_string):
    binary_array = int.from_bytes(input_string,"big")
    output_string = bin(binary_array)
    return output_string

def hamming_distance(s1,s2):
    j = 0
    ans = 0
    for i in s1:
        if i != s2[j]:
            ans = ans + 1
        j = j+1
    return ans

def repeat_xor(input_bytes,key):
    ans = b''
    j=0
    print(len(key))
    for i in input_bytes:
        ans += bytes([i^ord(key[j])])
        j = j + 1
        j = j % len(key)
    return ans

def main():
    encoded_text = open('6.txt','rb')
    original_text = encoded_text.read()
    decoded_base64 = base64.b64decode(original_text)
    possible_key_size = []
    for i in range(2,41):
        str1 = decoded_base64[:i:]
        str2 = decoded_base64[i:2*i:]
        str3 = decoded_base64[2*i:3*i:]
        str4 = decoded_base64[3*i:4*i:]
        score1 = hamming_distance(str1,str2)
        score2 = hamming_distance(str1,str3)
        score3 = hamming_distance(str2,str3)
        score = (score1+score2+score3)/3
        normalized_score = score/i
        data = {
            'score':normalized_score,
            'key_size':i
        }
        possible_key_size.append(data)
    sorted_key_list = sorted(possible_key_size,key = lambda x:x['score'])
    key_sz = sorted_key_list[0]['key_size']
    print("Key size found="+str(key_sz))
    blocks = []
    for i in range(key_sz+1):
        blocks.append(b'')
    j = 0
    for i in decoded_base64:
        blocks[j] += bytes([i])
        j = j + 1
        j = j % key_sz
    possible_message = []
    for block in blocks:
        possible_decodes = []
        for key in range(256):
            xorred_text = single_byte_xor(block,key)
            score = get_english_score(xorred_text)
            data = {
                'score':score,
                'xorred_text':xorred_text,
                'key':key
            }
            possible_decodes.append(data)
        sorted_decodes=sorted(possible_decodes,key=lambda x:x['score'],reverse=True)
        possible_message.append(sorted_decodes[0])
    final_key = ''
    for i in range(key_sz):
        final_key += chr(possible_message[i]['key'])
    print("Final Key = " + final_key)
    final_key =final_key.replace("\n"," ")
    #print(len(final_key))
    final_answer = repeat_xor(decoded_base64,final_key)
    print("Final Answer = " + str(final_answer))
    encoded_text.close()

if __name__ == '__main__':
    main()

