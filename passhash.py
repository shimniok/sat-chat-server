#!/usr/bin/env python3

from werkzeug.security import generate_password_hash
from sys import argv, exit

if len(argv) < 2:
	print("usage: passhash.py password")
	exit(2)

print(argv[1])
hash=generate_password_hash(argv[1], method='sha256')

print(hash)
