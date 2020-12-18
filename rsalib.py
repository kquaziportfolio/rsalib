import rsa


def keygen(size=512):
    pubkey, privkey = rsa.newkeys(size)
    n, e = pubkey.n, pubkey.e
    d, p, q = privkey.d, privkey.p, privkey.q
    return n, e, d, p, q, pubkey, privkey


def encrypt(message, n, e):
    pub_key = rsa.PublicKey(n, e)
    if type(message) == type("HI"):
        message = message.encode("utf-8")
    elif type(message) == type("1".encode("utf-8")):
        pass
    else:
        raise Exception("Please format your message to binary or string")
    message = rsa.encrypt(message, pub_key)
    return message


def decrypt(message, n, e, d, p, q):
    priv_key = rsa.PrivateKey(n, e, d, p, q)
    if type(message) == type("HI"):
        message = message.encode("utf-8")
    elif type(message) == type("1".encode("utf-8")):
        pass
    else:
        raise Exception("Please format your message to binary or string")
    return rsa.decrypt(message, priv_key)


def decryptformed(message, priv_key):
    if type(message) == type("HI"):
        message = message.encode("utf-8")
    elif type(message) == type("1".encode("utf-8")):
        pass
    else:
        raise Exception("Please format your message to binary or string")
    return rsa.decrypt(message, priv_key)


def signmessage(message, priv_key, hash_type="SHA-1"):
    if type(message) == type("1"):
        message = message.encode("UTF-8")
    return rsa.sign(message, priv_key, hash_type)


def verifymessage(message, sig, n, e):
    pub_key = rsa.PublicKey(n, e)
    if type(message) == type("1"):
        message = message.encode("utf-8")
    if type(sig) == type("1"):
        sig = sig.encode("utf-8")
    return rsa.verify(message, sig, pub_key)


def pubinfo(pub_key):
    with open(pub_key) as f:
        pubkey = rsa.PublicKey.load_pkcs1(f.read())
    return pubkey.n, pubkey.e


def privinfo(priv_key):
    with open(priv_key) as f:
        privkey = rsa.PrivateKey.load_pkcs1(f.read())
    n, e, d, p, q = privkey.n, privkey.e, privkey.d, privkey.p, privkey.q
    return n, e, d, p, q


if __name__ == "__main__":
    print("Do not run this as a cli")
