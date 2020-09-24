import base64

def encrypt(password):
    byteString = password.encode(encoding="utf-8")
    encodestr = base64.b64encode(byteString)
    return encodestr.decode()

def decrypt(password):
    encodestr = password.encode(encoding="utf-8")
    decodestr = base64.b64decode(encodestr)
    return decodestr.decode()