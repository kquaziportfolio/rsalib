# rsalib
This is a project built on top of the <a href="https://pypi.org/project/rsa/">RSA</a> Python library that includes a library for code to use (rsalib.py), a CLI built on top of the
library (rsacli.py), a WIP interactive shell (rsashell.py), a simple RSA cracker (rsacrack.py), a fast generator of primes (fastgen.py), and a simple hashing cli built ontop of
Python's builtin Hashlib (quickhash.py).

##Security Note
I wouldn't recommen using this library in production until RSA gets patched and fixes [CVE-2020-25658](https://nvd.nist.gov/vuln/detail/CVE-2020-25658).