import time
from itertools import count

import click
import click_spinner

click.arg = click.argument


def genpls():
    """
    Generator that yields primes relatively quickly.
    """
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


@click.command()
@click.arg("num")
@click.arg("out", default="-", type=click.File("w"))
def main(num, out):
    """
    Generates NUM prime numbers and stores them in OUT
    """
    num = int(num)
    g = genpls()
    c = time.time()
    t = next(g)
    a = 1
    while t <= num:
        out.write(str(t) + "\n")
        if a % 100000 == 0:
            print(
                "Num:",
                t,
                "Time:",
                time.time() - c,
                "Num of primes gen:",
                a,
                "\n\n",
                sep="\n",
            )
        t = next(g)
        a += 1
    print("Done!")
    print("Took", time.time() - c, "seconds to compute", a, "primes up to", num)


if __name__ == "__main__":
    main()
