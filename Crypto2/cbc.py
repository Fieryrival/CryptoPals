from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode
import json

data = b"secret"
key = b"YELLOW_SUBMARINE"
cipher = AES.new(key, AES.MODE_CBC)
ct_bytes = cipher.encrypt(pad(data, AES.block_size))
iv = b64encode(cipher.iv)
ct = b64encode(ct_bytes)
# result = json.dumps({'iv':iv, 'ciphertext':ct})

print(iv, iv.decode('utf-8'), len(cipher.iv))
print(ct)
