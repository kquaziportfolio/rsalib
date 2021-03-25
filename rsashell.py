import os
import subprocess as sp
import sys
import time
from cmd import Cmd

import rsa

import rsalib


class RSACmd(Cmd):
    """
    Main shell class
    """

    prompt = "rsa>"

    def do_exit(self, inp):
        """ Exits"""
        raise KeyboardInterrupt

    def do_shell(self, inp):
        """Spawns a shell"""
        sp.run("cmd")

    def do_keygen(self, inp):
        """Generates keys"""
        size, priv_key, pub_key = inp.split(" ")
        size = int(size)
        n, e, d, p, q, pubkey, privkey = rsalib.keygen(size)
        with open(pub_key, "wb") as f:
            f.write(pubkey.save_pkcs1())
        with open(priv_key, "wb") as f:
            f.write(privkey.save_pkcs1())
        print("E:\n", e, "\nN:\n", n, "\nD:\n", d, "\nP\n:", p, "\nQ:\n", q)

    def do_encrypt(self, inp):
        """Encrypts message with key"""
        message, pub_key, output = inp.split(" ")
        with open(pub_key) as f:
            pubkey = rsa.PublicKey.load_pkcs1(f.read())
        crypto = rsalib.encrypt(message, pubkey.n, pubkey.e)
        with open(output, "wb") as f:
            f.write(crypto)
        print("File written")

    def do_exec(self, inp):
        """Executes a single command in python (non persistant)"""
        exec(inp)

    def do_pyshell(self, inp):
        """Spawns a python shell"""
        sp.run("python")

    def do_run(self, inp):
        """Run a shell command"""
        sp.run(inp, shell=True)

    def do_decrypt(self, inp):
        """Decrypt"""
        inp = inp.split(" ")

    do_q = do_e = do_exit = do_x = do_exit
    do_EOF = do_exit


def recloop(dens=-1):
    """
    Runs the shell over and over again
    """
    if dens == 0:
        return
    try:
        RSACmd().cmdloop()

    except KeyboardInterrupt:
        print("Bye!")
        return
    except Exception as e:
        print(repr(e))
        recloop(dens - 1)


if __name__ == "__main__":
    density = -1
    if len(sys.argv) != 1:
        density = int(sys.argv[1])
    recloop(dens=density)
