__author__ = 'irmo'
import random
import tkinter as tk
import tkinter.filedialog
# 128 bit RSA algorithm

print("Hello, RSA!")


def miller_rabin(n, c=100):
    """
    :param n: the number needed to be test
    :param c: test count, default value is 100
    :return: whether n is a prime after c tests
    """

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
    """
    :param l: length
    :return: a binary prime of length l
    """
    while True:
        x = random.randrange(2 ** l, 2 ** (l + 1))
        if miller_rabin(x):
            return x


def generating_key():
    """
    p, q is two large prime.
    using p,q to generate RSA key.
    :return: RSA Public Key n, e, and RSA Private Key d
    """

    def extend_gcd(a, b):
        """
        :param a: ax + by = gcd
        :param b: ax + by = gcd
        :return: x, y, gcd
        """
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


# e is public key
def encrypt(m, e, n):
    return pow(m, e, n)


# d is private key
def decrypt(c, d, n):
    return pow(c, d, n)


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)



app = Application()
app.master.title('RSA with DES')
app.mainloop()