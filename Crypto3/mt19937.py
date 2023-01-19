import struct
import array


class MT19937:
    def __init__(self, seed) -> None:
        self.index = 624
        self.mt = [0]*624
        self.mt[0] = seed
        for i in range(1, 624):
            self.mt[i] = (0x6c078965*(self.mt[i-1] ^
                          (self.mt[i-1] >> 30)+i)) & 0xffffffff

    def extract_number(self):
        if self.index >= 624:
            self.generate_numbers()
        y = self.mt[self.index]
        y = y ^ (y >> 11)
        y = y ^ ((y << 7) & 0x9d2c5680)
        y = y ^ ((y << 15) & 0xefc60000)
        y = y ^ (y >> 18)
        self.index = self.index+1
        return y

    def generate_numbers(self):
        for i in range(624):
            y = (self.mt[i] & 0x80000000)+(self.mt[(i+1) % 624] & 0x7fffffff)
            self.mt[i] = self.mt[(i+397) % 624] ^ (y >> 1)
            if (y % 2) != 0:
                self.mt[i] = self.mt[i] ^ 0x9908b0df
        self.index = 0


def main():
    generator = MT19937(420)
    random_int = generator.extract_number()
    print(type(random_int),random_int)
    pass


if __name__ == '__main__':
    main()
