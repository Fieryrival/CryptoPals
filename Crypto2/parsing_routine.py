import json
import re
import os
import random
import string

def random_aes_key():
    res = ''.join(random.choices(string.ascii_uppercase +
                  string.ascii_lowercase + string.digits, k=16))
    return res

def email_filter(input_data):
    # email_id = "foobar@gmail.net&role=admin"
    email_regex = re.compile('^.+@.+(\.com)')
    mo = email_regex.search(input_data)
    return mo


def profile_for(email_address):
    # dict_of_data ={}
    dict_of_data = {
        'email': email_address,
        'uid': 10,
        'role': 'user'
    }
    res = ''
    # json_data = json.dumps(dict_of_data, indent=3)
    for k in dict_of_data.keys():
        if k == 'email':
            res += 'email='+dict_of_data[k]
        if k == 'uid':
            res += '&uid='+str(dict_of_data[k])
        if k == 'role':
            res += '&role='+dict_of_data[k]
    # res =res [:-1]
    # print(res)
    return res


def encode_profile_for(input_json):
    dict_data = json.loads(input_json)
    return dict_data
    pass


def kv_parser(input_bytes):
    for i in input_bytes:
        list_of_data = i.split(b'&')
        dict_of_data = {}
        for j in list_of_data:
            # print(j)
            key = j.split(b'=')[0]
            # print(key)
            key = key.decode()
            value = j.split(b'=')[1]
            value = value.decode('utf-8')
            data = {
                key: value
            }
            dict_of_data.update(data)
    # print(dict_of_data)
    json_object = json.dumps(dict_of_data, indent=4)
    return json_object



def main():
    in_file = open('/home/noob/Documents/Crypto2/parsing_input.txt', 'rb')
    list_of_inputs = in_file.readlines()
    in_file.close()
    json_object = kv_parser(list_of_inputs)
    email_id = "foobar@gmail.com&role=admin"
    filtered_mail = email_filter(email_id).group()
    # print(filtered_mail)
    profile_object = profile_for(filtered_mail)
    # print(profile_object)
    key = random_aes_key()
    print(key)

    # print(json_redict.keys())


if __name__ == '__main__':
    main()
