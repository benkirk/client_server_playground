#!/usr/bin/env python3

from multiprocessing.connection import Client
import time
import random
import os, sys
import sys

servers = ['foobar',
           'localhost',
           'casper-login1', 'casper-login2',
           'derecho1', 'derecho2', 'derecho3', 'derecho4',
           'derecho5', 'derecho6', 'derecho7', 'derecho8' ]

my_pid = os.getpid()

exe = sys.argv.pop(0)
cmd = '/opt/pbs/bin/qstat'
args = [ cmd ]
args.extend(sys.argv)

print(exe,args)

for server in servers:
    address = (server, 6000)
    try:
        with Client(address, authkey=b'secret password') as conn:
            print('Connected to \"{}\"'.format(server))
            conn.send((cmd, args))
            reply = conn.recv()

            if reply[0]: print(reply[0], end='', file=sys.stdout)
            if reply[1]: print(reply[1], end='', file=sys.stderr)
        sys.exit(0)

    except Exception as e:
        print('Cannot connect to \"{}\", {}'.format(server,e), file=sys.stderr)
        #raise

print('Could not connect to any servers, is the server process started??', file=sys.stderr)
sys.exit(1)
