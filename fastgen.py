from itertools import count
import time


def genpls():
    yield 2
    yield 3
    yield 5
    sieve = {}
    ps = genpls()
    p = next(ps) and next(ps)
    q = p * p
    for c in count(7, 2):
        if c in sieve:
            s = sieve.pop(c)
        elif c < q:
            yield c
            continue
        else:
            s = count(q + 2 * p, 2 * p)
            p = next(ps)
            q = p * p
        for m in s:
            if m not in sieve:
                break
        sieve[m] = s


import click

click.arg = click.argument


@click.command()
@click.arg("num")
@click.arg("out", type=click.File("w"))
def main(num, out):
    num = int(num)
    g = genpls()
    c = time.time()
    t = next(g)
    a = 1
    while t <= num:
        out.write(str(t) + "\n")
        t = next(g)
        a += 1
    print("Done!")
    print("Took", time.time() - c, "seconds to compute", a, "primes up to", num)


main()
