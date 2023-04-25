#ECB

from Crypto.Cipher import AES 
from Crypto.Hash import SHA256

#use SHA256 to hash the key to 32 bit long charaters, in bytes

def hash_key(key):
    hash_obj = SHA256.new(key.encode('utf-8'))
    hkey = hash_obj.digest()
    return hkey


def encrypt(info, secret_key):
    msg = info
    BLOCK_SIZE = 16
    PAD = '{'
    padding = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PAD
    hkey = hash_key(secret_key)
    print('encode hkey: ', hkey)
    cipher_text = AES.new(hkey, AES.MODE_ECB)
    results = cipher_text.encrypt(padding(msg).encode('utf-8'))
    return results
    


#result = msg + (block_size - len(msg) % block_size) * 'padding' 
#to padd the bit that is equal to multiple of block size

