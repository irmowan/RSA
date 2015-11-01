__author__ = 'irmo'
import random

# 128 bit RSA algorithm

print("Hello, RSA!")


# e is public key
def encrypt(m, e, n):
    return pow(m, e, n)


# d is private key
def decrypt(c, d, n):
    return pow(c, d, n)


def miller_rabin(n, c=100):
    def mr_test(n, m, k, a):
        b = pow(a, m, n)
        if b == 1:
            return True
        for j in range(1, k):
            if b == n - 1:
                return True
            b = (b * b) % n
        return b == n - 1

    if n % 2 == 0:
        return False

    # n = (2 ** k) * m + 1
    m, k = n - 1, 0
    while m % 2 == 0:
        m >>= 1
        k += 1
    for i in range(c):
        a = random.randint(2, n - 2)
        if not mr_test(n, m, k, a):
            return False
    return True


def random_prime(len):
    while True:
        x = random.randrange(2 ** len, 2 ** (len + 1))
        if miller_rabin(x):
            return x


test = 300
from time import clock

start = clock()
for i in range(test):
    x = random_prime(64)
    print(x)

finish = clock()
print((finish - start))
