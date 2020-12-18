import click, math, rsa, time
from itertools import count
from sympy import mod_inverse

click.arg = click.argument
"""
def genpls():
    yield 2; yield 3; yield 5;
    sieve = {}
    ps = genpls()
    p = next(ps) and next(ps)
    q = p*p
    for c in count(7,2):
        if c in sieve:
            s = sieve.pop(c)
        elif c < q:
             yield c
             continue
        else:
            s=count(q+2*p,2*p)
            p=next(ps)
            q=p*p
        for m in s:
            if m not in sieve:
                break
        sieve[m] = s
"""
#'''
def genpls():
    yield from (2, 3)
    i = 1
    while True:
        yield 6 * i - 1
        yield 6 * i + 1
        i += 1


#'''
"""
import itertools as it
def genpls( ):
    D = { 9: 3, 25: 5 }
    yield 2
    yield 3
    yield 5
    MASK= 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0,
    MODULOS= frozenset( (1, 7, 11, 13, 17, 19, 23, 29) )

    for q in it.compress(
            it.islice(it.count(7), 0, None, 2),
            it.cycle(MASK)):
        p = D.pop(q, None)
        if p is None:
            D[q*q] = q
            yield q
        else:
            x = q + 2*p
            while x in D or (x%30) not in MODULOS:
                x += 2*p
            D[x] = p
"""


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("No modular inverse")
    return x % m


def genprimes(n):
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
    pass


@main.command()
@click.arg("n")
@click.arg("e")
@click.option("--outf", "-o", default=None)
def crack(n, e, outf):
    print("No longer supported")
    return
    st = time.time()
    n = int(n)
    e = int(e)
    sqrtn = float(repr(math.sqrt(n)))
    c = int(sqrtn - (sqrtn % 1))
    if c % 2 == 0:
        c -= 1
    print("Cracking Started")
    count = 0
    for i in range(c, 3, -2):
        if n % i == 0:
            print("Solution found:\n" + str(i), n % i)
            break
        if count % 100000 == 0:
            print(i, n % i)
        count += 1
    p = i
    q = n / p
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
    print("Cracking took", time.time() - st)
    if outf == None:
        return
    with open(outf, "wb") as f:
        key = rsa.PrivateKey(n, e, d, p, q)
        f.write(key.save_pkcs1())


@main.command()
@click.arg("i")
@click.option("--outf", "-o", default=None)
def fcrack(i, outf):
    st = time.time()
    with open(i) as f:
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
    for i in genpls():
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
    if outf == None:
        return
    with open(outf, "wb") as f:
        key = rsa.PrivateKey(n, e, d, p, q)
        f.write(key.save_pkcs1())


if __name__ == "__main__":
    main()
