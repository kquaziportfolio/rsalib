import time

import click
import click_didyoumean
import click_spinner
import rsa
from colorama import Back, Fore, Style, init
from pyfiglet import Figlet

import rsalib

init(autoreset=True)
click.arg = click.argument
__version__ = "1.0.0"


@click.group(cls=click_didyoumean.DYMGroup)
@click.option("--no-banner", "no_banner", is_flag=True)
def main(no_banner):
    if not (no_banner):
        f = Figlet(font="banner3-D")
        print(Fore.GREEN + f.renderText("RSA-CLI Version " + __version__))


@main.command()
@click.arg("size", type=int)
@click.arg("priv_key")
@click.arg("pub_key")
def keygen(size, priv_key, pub_key):
    initial_time = time.time()
    print("Generating key...")
    with click_spinner.spinner():
        n, e, d, p, q, pubkey, privkey = rsalib.keygen(size)
    with open(pub_key, "wb") as f:
        f.write(pubkey.save_pkcs1())
    with open(priv_key, "wb") as f:
        f.write(privkey.save_pkcs1())
    print("E:\n", e, "\nN:\n", n, "\nD:\n", d, "\nP:\n", p, "\nQ:\n", q)
    print("\nTook", time.time() - initial_time, "seconds to generate")


@main.command()
@click.arg("messagef", type=click.File("rb"))
@click.arg("pub_key", type=click.File())
@click.arg("output", type=click.File("wb"))
def encrypt(messagef, pub_key, output):
    pubkey = rsa.PublicKey.load_pkcs1(pub_key.read())
    crypto = rsalib.encrypt(messagef.read(), pubkey.n, pubkey.e)
    output.write(crypto)
    print("File written")


@main.command()
@click.arg("crypto", type=click.File("rb"))
@click.arg("priv_key", type=click.File())
@click.arg("outfile", type=click.File("w"))
def decrypt(crypto, priv_key, outfile):
    privkey = rsa.PrivateKey.load_pkcs1(priv_key.read())
    crypted = crypto.read()
    message = rsalib.decryptformed(crypted, privkey)
    outfile.write(message.decode())


@main.command()
@click.arg("message", type=click.File("rb"))
@click.arg("priv_key", type=click.File())
@click.arg("output", type=click.File("wb"))
@click.option("--hashtype", "-h", default="SHA-256")
def sign(message, priv_key, output, hashtype):
    privkey = rsa.PrivateKey.load_pkcs1(priv_key.read())
    sig = rsalib.signmessage(message.read(), privkey, hashtype)
    output.write(sig)
    print("File writen")


@main.command()
@click.arg("message", type=click.File("rb"))
@click.arg("sig_file", type=click.File("rb"))
@click.arg("pub_key", type=click.File())
def verify(message, sig_file, pub_key):
    pubkey = rsa.PublicKey.load_pkcs1(pub_key.read())
    sig = sig_file.read()
    try:
        rsalib.verifymessage(message, sig, pubkey.n, pubkey.e)
    except rsa.VerificationError:
        print(
            """An error has occured. The message is most likely cause is that
the message has been forged or tampered with. Do not trust the
message and beware of the MITM (Man in the Middle) attack."""
        )
        # raise
        return
    print("The hash type is:", rsalib.verifymessage(message, sig, pubkey.n, pubkey.e))
    print("The message has been verified. Happy encryption")


@main.command()
@click.arg("pubkey", type=click.File())
def pubinfo(pubkey):
    n, e = rsalib.pubinfo(pubkey.read())
    print("E:\n", e, "\nN:\n", n)


@main.command()
@click.arg("privkey", type=click.File())
def privinfo(privkey):
    n, e, d, p, q = rsalib.privinfo(privkey.read())
    print("Size is: ", n.bit_length(), "\n")
    print("E:\n", e, "\nN:\n", n, "\nD:\n", d, "\nP:", p, "\nQ:\n", q)


if __name__ == "__main__":
    main()
