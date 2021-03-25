import hashlib

import click


@click.command()
@click.argument("hashtype", type=str)
@click.argument("file", type=click.File("rb"), default="-")
@click.option("--output", "-o", "out", type=click.File("w"), default="-")
def entrypoint(hashtype: str, file, out):
    """
    Hashes FILE using the algorithm specified by HASHTYPE and stores it in OUT (defaults to stdout)
    """
    if hashtype not in hashlib.algorithms_guaranteed:
        print("Invalid hashing algorithm")
    try:
        out.write(getattr(hashlib, hashtype)(file.read()).hexdigest())
    except TypeError:
        out.write(getattr(hashlib, hashtype)(file.read()).hexdigest(16))


if __name__ == "__main__":
    entrypoint()
