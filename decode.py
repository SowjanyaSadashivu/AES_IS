from Crypto.Cipher import AES 
from Crypto.Hash import SHA256

def hash_key(key):
    hash_obj = SHA256.new(key.encode('utf-8'))
    hkey = hash_obj.digest()
    return hkey

def decrypt(info, secret_key):
    msg = info
    pad = '{'
    hkey = hash_key(secret_key)
    print("decrypt message :",msg)
    decipher = AES.new(hkey, AES.MODE_ECB)
    print('decode hkey: ',hkey)
    print("type of decrypted msg",type(msg))
    pt = decipher.decrypt(msg).decode('utf-8')
    pad_index = pt.find(pad)
    result = pt[:pad_index]
    return result
   
    