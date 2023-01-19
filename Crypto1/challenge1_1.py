import base64

encoded_string = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
target = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"

step1 = bytes.fromhex(encoded_string) #convert to bytes
step2 = base64.b64encode(step1) #convert to base64
step3 = step2.decode('utf-8') #convert to text
print(type(step1))
print(step3)

if step2.decode('utf-8') == target:
    print("Done")
