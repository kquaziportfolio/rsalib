import hashlib

import click


@click.group()
def entrypoint():
    pass


@entrypoint.command()
@click.argument("file", type=click.File("rb"), default="-")
@click.option("--output", "-o", "out", type=click.File("w"), default="-")
def sha256(file, out):
    out.write(hashlib.sha256(file.read()).hexdigest())


@entrypoint.command()
@click.argument("file", type=click.File("rb"), default="-")
@click.option("--output", "-o", "out", type=click.File("w"), default="-")
def sha1(file, out):
    out.write(hashlib.sha1(file.read()).hexdigest())


@entrypoint.command()
@click.argument("file", type=click.File("rb"), default="-")
@click.option("--output", "-o", "out", type=click.File("w"), default="-")
def md5(file, out):
    out.write(hashlib.md5(file.read()).hexdigest())


if __name__ == "__main__":
    entrypoint()
