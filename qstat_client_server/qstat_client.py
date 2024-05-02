#!/usr/bin/env python3

from multiprocessing.connection import Client
import time
import random
import os, sys
import sys

address = ('casper-login2', 6000)

my_pid = os.getpid()

exe = sys.argv.pop(0)
cmd = '/opt/pbs/bin/qstat'
args = [ cmd ]
args.extend(sys.argv)

print(exe,args)

try:
    with Client(address, authkey=b'secret password') as conn:

        conn.send((cmd, args))
        reply = conn.recv()

        if reply[0]: print(reply[0], end='', file=sys.stdout)
        if reply[1]: print(reply[1], end='', file=sys.stderr)

except ConnectionRefusedError as e:
    raise
