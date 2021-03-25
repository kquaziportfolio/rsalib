import typing

import rsa


def keygen(
    size: int = 512,
) -> typing.Tuple[int, int, int, int, int, rsa.PublicKey, rsa.PrivateKey]:
    """
    Generate a keypair of size SIZE
    """
    pubkey, privkey = rsa.newkeys(size)
    n, e = pubkey.n, pubkey.e
    d, p, q = privkey.d, privkey.p, privkey.q
    return int(n), int(e), d, p, q, pubkey, privkey


def encrypt(message: typing.Union[str, bytes], n: int, e: int) -> bytes:
    """
    Encrypt MESSAGE with public key specified by N and E
    """
    pub_key = rsa.PublicKey(n, e)
    if isinstance(message, str):
        message = message.encode("utf-8")
    elif isinstance(message, bytes):
        pass
    else:
        raise Exception("Please format your message to binary or string")
    message = rsa.encrypt(message, pub_key)
    return message


def decrypt(
    message: typing.Union[str, bytes], n: int, e: int, d: int, p: int, q: int
) -> bytes:
    """
    Decrypt MESSAGE with private key specified by N, E, D, P, and Q
    """
    priv_key = rsa.PrivateKey(n, e, d, p, q)
    if isinstance(message, str):
        message = message.encode("utf-8")
    elif isinstance(message, bytes):
        pass
    else:
        raise Exception("Please format your message to binary or string")
    return rsa.decrypt(message, priv_key)


def decryptformed(message: typing.Union[str, bytes], priv_key: rsa.PrivateKey) -> bytes:
    """
    Decrypt MESSAGE with private key specified by priv_key
    """
    if isinstance(message, str):
        message = message.encode("utf-8")
    elif isinstance(message, bytes):
        pass
    else:
        raise Exception("Please format your message to binary or string")
    return rsa.decrypt(message, priv_key)


def signmessage(
    message: typing.Union[str, bytes],
    priv_key: rsa.PrivateKey,
    hash_type: str = "SHA-1",
) -> bytes:
    """
    Signs MESSAGE with private key in PRIV_KEY and hash type HASH_TYPE
    """
    if isinstance(message, str):
        message = message.encode("UTF-8")
    return rsa.sign(message, priv_key, hash_type)


def verifymessage(
    message: typing.Union[str, bytes], sig: typing.Union[str, bytes], n: int, e: int
) -> str:
    """
    Verifies MESSAGE/SIG pair with public key in N + E
    """
    pub_key = rsa.PublicKey(n, e)
    if isinstance(message, str):
        message = message.encode("utf-8")
    if isinstance(sig, str):
        sig = sig.encode("utf-8")
    return rsa.verify(message, sig, pub_key)


def pubinfo(pub_key: bytes) -> typing.Tuple[int, int]:
    """
    Gets public key info of PUB_KEY
    """
    pubkey = rsa.PublicKey.load_pkcs1(pub_key)
    return pubkey.n, pubkey.e


def privinfo(priv_key: bytes) -> typing.Tuple[int, int, int, int, int]:
    """
    Gets private key info of PRIV_KEY
    """
    privkey = rsa.PrivateKey.load_pkcs1(priv_key)
    n, e, d, p, q = privkey.n, privkey.e, privkey.d, privkey.p, privkey.q
    return n, e, d, p, q


if __name__ == "__main__":
    print("Do not run this as a cli")
