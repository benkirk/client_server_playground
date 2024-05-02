#!/usr/bin/env python3

from multiprocessing.connection import Client
from array import array
import time
import random
import os

address = ('localhost', 6000)

my_pid = os.getpid()

for cnt in range(5000):

    try:
        with Client(address, authkey=b'secret password') as conn:

            conn.send(('foo', 'request from {}, local step {}'.format(my_pid,cnt)))
            reply = conn.recv()
            print(reply)

        time.sleep(random.uniform(0.,0.02))

    except ConnectionRefusedError as e:
        raise
