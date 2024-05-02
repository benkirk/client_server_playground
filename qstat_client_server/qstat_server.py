#!/usr/bin/env python3

from multiprocessing.connection import Listener
import time
import random
import subprocess
from functools import lru_cache, wraps
from datetime import datetime, timedelta, UTC

CACHE_TIMEOUT = 2 # seconds
CACHE_SIZE = 256 # cached entries

address = ('', 6000)     # family is deduced to be 'AF_INET'

trusted_exe = set(['qstat',
                   'ls',
                   '/opt/pbs/bin/qstat'])

# https://realpython.com/lru-cache-python/#adding-cache-expiration
def timed_lru_cache(seconds: int, maxsize: int = 128):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.now(UTC) + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.now(UTC) >= func.expiration:
                print(func.cache_info())
                func.cache_clear()
                func.expiration = datetime.now(UTC) + func.lifetime
            return func(*args, **kwargs)

        return wrapped_func
    return wrapper_cache




@timed_lru_cache(seconds=CACHE_TIMEOUT, maxsize=CACHE_SIZE)
def run_command(args):
    result = subprocess.run(args, capture_output=True, encoding='utf8')
    return result



with Listener(address,
              authkey=b'secret password',
              backlog=100) as listener:

    print('Waiting for connections...')
    ts = time.time()
    n_msgs = 0

    while True:
        with listener.accept() as conn:

            request = conn.recv()

            assert (type(request) is tuple)

            cmd = request[0]
            args = request[1:]


            # print('  --> {} asked me to run \"{} {}\"'.format(listener.last_accepted,
            #                                                   cmd,
            #                                                   args))

            n_msgs += 1
            elapsed = time.time() - ts
            rate = float(n_msgs) / elapsed
            now = datetime.now().isoformat(sep=' ', timespec='seconds')
            print('[{}] {:,}: [{:.2f} (msg/sec)], {} asked me to run \"{} {}\"'.format(now,
                                                                                       n_msgs,
                                                                                       rate,
                                                                                       listener.last_accepted,
                                                                                       cmd,
                                                                                       args))
            if cmd in trusted_exe:
                print('Trusted command \"{}\" will be excuted...'.format(cmd))
                #result = subprocess.run(request[1], capture_output=True, encoding='utf8')
                result = run_command(tuple(request[1]))
                #print(result.stdout)
                conn.send((result.stdout, result.stderr, result.returncode))

            else:
                print('Untrusted commnd \"{}\" rejected...'.format(cmd))
                conn.send('DENIED')
