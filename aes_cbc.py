# Written by Subin Jo
# 2022.11.27
# python3

from Cryptodome.Cipher import AES

class AES_CBC:
    BLOCK_SIZE = 16
    KEY_DIC = {'E2': ['756e617661696c61626c650000000000', b"0123456789abcdef"]}

    """def __init__(self, type):
        self.crypto = AES.new(self.KEY_DIC[type][0], AES.MODE_CBC, self.KEY_DIC[type][1])
"""

    def __init__(self, key, iv):
        self.crypto = AES.new(key, AES.MODE_CBC, iv)

    def decrypt(self, enc_buf):
        dec_buf = self.crypto.decrypt(enc_buf)
        return dec_buf

def divideType():
    return 0

def aes_decrypt(key, iv, in_f, out_path):
    BLOCK_SIZE = 16

    enc_buf = in_f.read(BLOCK_SIZE)
    if enc_buf is None or len(enc_buf) == 0:
        print("Empty File")
        return 0

    #aes = AES_CBC('E2')
    aes = AES_CBC(key, iv)
    print("complete aes new")
    dec_buf = aes.decrypt(enc_buf)
    first = dec_buf.decode('utf-8').rstrip('\x00')
    #print(first, type(first))

    # Check first 16bytes is timestamp
    # And then decrypt all file
    if first.isdigit():
        out_f = open(out_path, 'wb')
        enc_buf = in_f.read()
        dec_buf = aes.decrypt(enc_buf)
        out_f.write(dec_buf)
        out_f.close()





