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
        self.LabelTitile = tk.Label(self, text='RSA with DES')
        self.LabelSender = tk.Label(self, text='\n\nSender 发送方\n\n')
        self.LabelReceiver = tk.Label(self, text='\n\nReceiver 接收方\n\n')

        self.LabelSenderKey = tk.Label(self, text='密钥')
        self.LabelRSAKey = tk.Label(self, text='RSA加密后的密钥')
        self.LabelReceiverKey = tk.Label(self, text='密钥')

        self.LabelSenderText = tk.Label(self, text='明文')
        self.LabelDESText = tk.Label(self, text='DES加密后的密文')
        self.LabelReceiverText = tk.Label(self, text='明文')

        self.DESKeyButton = tk.Button(self, text='生成DES密钥', command=self.generating_DES_key)
        self.DualKeyText = tk.Text(self, width=45, height=6)
        self.LabelDualKey = tk.Label(self, text='接收方公钥及私钥')
        self.DualKeyButton = tk.Button(self, text='生成RSA双钥', command=self.generating_dual_key)

        self.RSAEncryptButton = tk.Button(self, text='RSA加密', command=self.RSA_encrypt)
        self.RSADecryptButton = tk.Button(self, text='RSA解密', command=self.RSA_decrypt)
        self.DESEncryptButton = tk.Button(self, text='DES加密', command=self.DES_encrypt)
        self.DESDecryptButton = tk.Button(self, text='DES解密', command=self.DES_decrypt)

        self.ReadTextButton = tk.Button(self, text='读入文本', command=self.open_text)
        self.SaveTextButton = tk.Button(self, text='保存文本', command=self.save_text)

        width, height = 30, 8
        self.SenderKeyText = tk.Text(self, width=width, height=height)
        self.RSAKeyText = tk.Text(self, width=width, height=height)
        self.ReceiverKeyText = tk.Text(self, width=width, height=height)

        self.SenderPlainText = tk.Text(self, width=width, height=height)
        self.DESCipherText = tk.Text(self, width=width, height=height)
        self.ReceiverPlainText = tk.Text(self, width=width, height=height)

        Readme = '''
        **使用说明**
        1.接收方生成128 bit双钥，包括公钥及私钥
        2.发送方生成64 bitDES密钥(用于加密文本)
        3.发送方利用接收方RSA公钥，加密DES key
        4.发送方利用原始的DES key，加密明文文本
        5.接收方利用自己的RSA私钥，解密DES key
        6.接收方利用解密出的DES key解密密文文本
        '''

        self.ReadmeLabel = tk.Label(self, text=Readme)
        self.create_widgets()
        self.grid()

    def create_widgets(self):
        # self.LabelTitile.grid(column=0, row=0, columnspan=5)
        self.LabelSender.grid(column=0, row=1)
        self.LabelReceiver.grid(column=4, row=1)

        self.LabelDualKey.grid(column=2, row=2)
        self.DESKeyButton.grid(column=0, row=3)
        self.DualKeyText.grid(column=1, row=3, columnspan=3)
        self.DualKeyButton.grid(column=4, row=3)

        self.LabelSenderKey.grid(column=0, row=4)
        self.LabelRSAKey.grid(column=2, row=4)
        self.LabelReceiverKey.grid(column=4, row=4)

        self.SenderKeyText.grid(column=0, row=5)
        self.RSAEncryptButton.grid(column=1, row=5)
        self.RSAKeyText.grid(column=2, row=5)
        self.RSADecryptButton.grid(column=3, row=5)
        self.ReceiverKeyText.grid(column=4, row=5)

        self.LabelSenderText.grid(column=0, row=6)
        self.LabelDESText.grid(column=2, row=6)
        self.LabelReceiverText.grid(column=4, row=6)

        self.SenderPlainText.grid(column=0, row=7)
        self.DESEncryptButton.grid(column=1, row=7)
        self.DESCipherText.grid(column=2, row=7)
        self.DESDecryptButton.grid(column=3, row=7)
        self.ReceiverPlainText.grid(column=4, row=7)

        self.ReadTextButton.grid(column=0, row=8)
        self.SaveTextButton.grid(column=4, row=8)
        self.ReadmeLabel.grid(column=1, row=9, columnspan=3)

    def generating_dual_key(self):
        pass

    def generating_DES_key(self):
        pass

    def RSA_encrypt(self):
        pass

    def RSA_decrypt(self):
        pass

    def DES_encrypt(self):
        pass

    def DES_decrypt(self):
        pass

    def open_text(self):
        pass

    def save_text(self):
        pass


app = Application()
app.master.title('RSA with DES')
app.mainloop()
