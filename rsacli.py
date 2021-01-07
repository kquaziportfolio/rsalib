import rsalib, time, click, rsa
from pyfiglet import Figlet
from colorama import init, Fore, Back, Style
init(autoreset=True)
click.arg = click.argument
__version__="1.0.0"

@click.group()
@click.option("--no-banner","no_banner",is_flag=True)
def main(no_banner):
    if not(no_banner):
        f=Figlet(font="banner3-D")
        print(Fore.GREEN+f.renderText("RSA-CLI Version "+__version__))

@main.command()
@click.arg("size", type=int)
@click.arg("priv_key")
@click.arg("pub_key")
def keygen(size, priv_key, pub_key):
    print("Generating key...")
    n, e, d, p, q, pubkey, privkey = rsalib.keygen(size)
    with open(pub_key, "wb") as f:
        f.write(pubkey.save_pkcs1())
    with open(priv_key, "wb") as f:
        f.write(privkey.save_pkcs1())
    print("E:\n", e, "\nN:\n", n, "\nD:\n", d, "\nP:\n", p, "\nQ:\n", q)


@main.command()
@click.arg("message")
@click.arg("pub_key")
@click.arg("output")
def encrypt(message, pub_key, output):
    with open(pub_key) as f:
        pubkey = rsa.PublicKey.load_pkcs1(f.read())
    crypto = rsalib.encrypt(message, pubkey.n, pubkey.e)
    with open(output, "wb") as f:
        f.write(crypto)
    print("File written")


@main.command()
@click.arg("crypto")
@click.arg("priv_key")
def decrypt(crypto, priv_key):
    print("Message says:")
    with open(priv_key) as f:
        privkey = rsa.PrivateKey.load_pkcs1(f.read())
    with open(crypto, "rb") as f:
        crypted = f.read()
    message = rsalib.decryptformed(crypted, privkey)
    print(message.decode())


@main.command()
@click.arg("message")
@click.arg("priv_key")
@click.arg("output")
@click.option("--hashtype", "-h", default="SHA-256")
def sign(message, priv_key, output, hashtype):
    with open(priv_key) as f:
        privkey = rsa.PrivateKey.load_pkcs1(f.read())
    sig = rsalib.signmessage(message, privkey, hashtype)
    with open(output, "wb") as f:
        f.write(sig)
    print("File writen")


@main.command()
@click.arg("message")
@click.arg("sig_file")
@click.arg("pub_key")
def verify(message, sig_file, pub_key):
    with open(pub_key) as f:
        pubkey = rsa.PublicKey.load_pkcs1(f.read())
    with open(sig_file, "rb") as f:
        sig = f.read()
    try:
        rsalib.verifymessage(message, sig, pubkey.n, pubkey.e)
    except rsa.VerificationError:
        print(
            """An error has occured. The message is most likely cause is that
the message has been forged or tampered with. Do not trust the
message and beware of the MITM (Man in the Middle) attack."""
        )
        return
    print("The hash type is:", rsalib.verifymessage(message, sig, pubkey.n, pubkey.e))
    print("The message has been verified. Happy encryption")


@main.command()
@click.arg("pubkey")
def pubinfo(pubkey):
    n, e = rsalib.pubinfo(pubkey)
    print("E:\n", e, "\nN:\n", n)


@main.command()
@click.arg("privkey")
def privinfo(privkey):
    n, e, d, p, q = rsalib.privinfo(privkey)
    print("Size is: ", n.bit_length(), "\n")
    print("E:\n", e, "\nN:\n", n, "\nD:\n", d, "\nP:", p, "\nQ:\n", q)


if __name__ == "__main__":
    main()