def pad(input_bytes: bytes, block_size: int) -> bytes:
    padding = block_size - (len(input_bytes) % block_size)
    return input_bytes + bytes([padding]*padding)


def unpad(input_bytes: bytes, block_size: int) -> bytes:
    len = 0
    reversed_bytes = input_bytes[-1]
    return input_bytes[:-input_bytes[-1]]  # didnt quite understand this....
    # return input_bytes[-reversed_bytes:] == bytes([reversed_bytes]) * reversed_bytes


def main():
    sample = b'YELLOW SUBMARINE'
    block_size = 20
    res = pad(sample, block_size)
    # orig = unpad(b'email=abbcd@cde.com&uid=10&role=admin\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c', 16)
    print(res)
    # print(orig)


if __name__ == '__main__':
    main()
