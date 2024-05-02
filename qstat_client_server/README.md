# `qstat` client/server query tool with server-side results caching

## Usage:

### Server
Start the server as a user with PBS Operator privileges, noting the server name you're on:
```pre
csgteam@casper-login2$ ./qstat_server
```
### Client
(Have look at `qstat_client.py` and make sure the host name in `address = ('casper-login2', 6000)` matches the server above.)
```pre
benkirk@derecho7(3)$ ./qstat_client -aw
```
Inspect the impact of caching by watching the server `stdout` while running the following:
```pre
benkirk@derecho7(3)$ while true; do ./qstat_client -aw; done
```
