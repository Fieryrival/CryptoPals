from Crypto.Cipher import AES
import base64

in_file = open('7.txt','rb')
text = in_file.read()

msg = base64.b64decode(text)

key = b'YELLOW SUBMARINE'

decipher = AES.new(key,AES.MODE_ECB)
print(decipher.decrypt(msg))
in_file.close()
