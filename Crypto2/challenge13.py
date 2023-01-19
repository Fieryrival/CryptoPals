import os
from Crypto.Cipher import AES
# import json
# from Crypto.Util.Padding import pad


def pad(input_bytes: bytes, block_size: int) -> bytes:
    padding = block_size - (len(input_bytes) % block_size)
    return input_bytes + bytes([padding]*padding)


def profile_for(email_id):
    if '&' in email_id or '=' in email_id:
        return 'Invalid email'
    else:
        return 'email=' + email_id + '&uid=10&role=user'


def aes_encrypt(user_profile, key):
    cipher = AES.new(key, AES.MODE_ECB)
    encoded_msg = cipher.encrypt(user_profile)
    return encoded_msg


def aes_decrypt_parse(encoded_user_profile, key):
    decipher = AES.new(key, AES.MODE_ECB)
    decoded_msg = decipher.decrypt(encoded_user_profile)
    new_decoded_msg = unpad(decoded_msg, AES.block_size)
    print(new_decoded_msg)
    decoded = new_decoded_msg.decode('utf-8')
    print(decoded)
    result = dict(pair.split('=') for pair in decoded.split('&'))
    return result
    # return


def random_aes_key():
    return os.urandom(16)


def unpad(input_bytes, block_size):
    rev = input_bytes[-1]
    return input_bytes[:-input_bytes[-1]]


def main():
    key = random_aes_key()
    # according to challenge we need to input encoded_data to get parsed data with role as admin
    # used \x0c as padding because default function was using this variable to pad the blocks
    email = 'abbcd@cde.'+'admin'+('\x0b'*11)+'com'
    url_data = profile_for(email)
    if url_data == 'Invalid email':
        print('Mail error')
        return
    url_data = url_data.encode()
    padded_data = pad(url_data, 16)
    print(padded_data)
    encoded_data = aes_encrypt(padded_data, key)
    hex_data = encoded_data.hex()
    print(hex_data, len(encoded_data), len(hex_data))
    # here i have passed or printed the encoded_data as hex and decoded it before decrypting
    # modified_data = input("The encrypted data by attacker = ")
    modified_data = hex_data[0:32]+hex_data[64:96]+hex_data[32:64]
    print(modified_data)
    modified_data = bytes.fromhex(modified_data)
    decoded_data = aes_decrypt_parse(modified_data, key)
    print(decoded_data)
    # dont know why but for some reason unpad is removing 'n' from admin
    #UPDATE : solved 'n' issue with correct padding byte \0xb


if __name__ == '__main__':
    main()
