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


def random_prime(l):
    while True:
        x = random.randrange(2 ** l, 2 ** (l + 1))
        if miller_rabin(x):
            return x


def generating_key():
    def extend_gcd(a, b):
        # ax + by = gcd
        # return x, y, gcd
        if b == 0:
            return 1, 0, a
        else:
            x, y, g = extend_gcd(b, a % b)
            return y, x - y * (a // b), g

    def inv(a, n):
        x, y, g = extend_gcd(a, n)
        if g == 1:
            return x % n
        else:
            return None

    p, q = 0, 0
    while p * q < 2 ** 127:
        p = random_prime(64)
        q = random_prime(64)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    d = random.randrange(1, phi_n)
    while inv(d, phi_n) is None:
        d = random.randrange(1, phi_n)
    e = inv(d, phi_n)
    print('Public  Key: ', 'n =', n, ', e =', e)
    print('Private Key: ', 'd =', d)
    return n, e, d


n, e, d = generating_key()
