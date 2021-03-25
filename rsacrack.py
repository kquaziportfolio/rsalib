import math
import time
import typing

import click
import rsa


def genprimes_generic():
    """Generates probable primes using 6*i +- 1"""
    yield 2
    yield 3
    i = 1
    while True:
        yield 6 * i - 1
        yield 6 * i + 1
        i += 1


def genprimes_file(f):
    """
    Generates primes from a given file that contains a list
    """
    with open(f) as file:
        for i in file:
            yield int(i)


def egcd(a: int, b: int) -> typing.Tuple[int, int, int]:
    """
    Calculates the Euclidean GCD of a and b
    """
    if a == 0:
        return b, 0, 1
    g, y, x = egcd(b % a, a)
    return g, x - (b // a) * y, y


def modinv(a: int, m: int) -> int:
    """
    Calculates the modular inverse of a and m
    """
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("No modular inverse")
    return x % m


def genprimes(n) -> typing.List:
    """
    A copy of the prime generator found in fastgen.py
    """
    primes = [2, 3]
    sqrtn = math.sqrt(n)
    c = int(sqrtn - (sqrtn % 1))
    if c % 2 == 0:
        c -= 1
    for i in range(c, 3, -2):
        if (i % 6 == 1) or (i % 6 == 5):
            primes.append(i)
    print("Primes generated\n")
    if n < 100000:
        print(primes)
    return primes


@click.group()
def main():
    """Main group"""
    pass


@main.command()
@click.argument("i")
@click.option("--outf", "-o", default=None)
@click.option("-p", "--primelist", default=None, type=click.Path())
def fcrack(i, outf, primelist):
    """
    Finds the private key of the public key in OUTF, optionally using PRIMELIST as a list of primes
    """
    if primelist is None:
        genpls = genprimes_generic()
    else:
        genpls = genprimes_file(primelist)
    st = time.time()
    with open(i, "rb") as f:
        privkey = rsa.PublicKey.load_pkcs1(f.read(), "PEM")
    n = privkey.n
    e = privkey.e
    print("N:", n)
    sqrtn = math.sqrt(n)
    c = int(sqrtn - (sqrtn % 1))
    sol = 0
    count = 0
    if c % 2 == 0:
        c -= 1
    print("Cracking Started")
    for i in genpls:
        if n % i == 0:
            print("Solution found:\n" + str(i), n % i)
            sol = 1
            break
        if count % 100000 == 0:
            print(i, n % i)
        count += 1
    if sol == 0:
        print("No solution, idk")
        return
    p = i
    q = int(n / p)
    assert p * q == n
    phin = (p - 1) * (q - 1)
    d = modinv(e, phin)
    p, q = q, p
    print("P: ", int(p))
    print("Q: ", int(q))
    print("Phi(n): ", repr(int(phin)))
    print("Coef: ", int(rsa.common.inverse(q, p)))
    print("Exp1: ", int(d % (p - 1)))
    print("Exp2: ", int(d % (q - 1)))
    print("D: ", int(d))
    print("Cracking took", time.time() - st, "seconds")
    if outf is None:
        return
    with open(outf, "wb") as f:
        key = rsa.PrivateKey(n, e, d, p, q)
        f.write(key.save_pkcs1())


if __name__ == "__main__":
    main()
