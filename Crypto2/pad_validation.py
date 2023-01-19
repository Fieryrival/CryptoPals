from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES


def check_2(text):
    return text[-1]*text[-1:] == text[-text[-1]:]

def check_padding(text):
    if text[-1] <= 16:
        if text[-1]*text[-1:] == text[-text[-1]:]:
            # function checks if text[-1:] which is byte string of last character
            # text[-1] gives the byte or int value of last character
            return "Valid Padding"
        else:
            raise Exception('Bad Padding')
    else:
        if len(text) % 16 == 0:
            return "No Padding"
        else:
            raise Exception('Invalid padding')


def main():
    text = b'ICE ICE BABY\x04\x04\x04\x00'
    print(text)
    # print (bytes([4]))
    # print(text[-text[-1]:])
    # def result(text): return text[-1:]*text[-1] == text[-text[-1]:]
    result = check_2(text)
    print(result)
    # print(result)


if __name__ == '__main__':
    main()
