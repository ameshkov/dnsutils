# DNS utils

## dnsload.py

Example: `python3 dnsload.py -s 8.8.8.8 -i 100`

```
$ python3 dnsload.py -h
Usage: dnsload.py [options]

Options:
  -h, --help            show this help message and exit
  -s SERVER, --server=SERVER
                        DNS server address.
  -i INTERVAL, --interval=INTERVAL
                        interval between DNS requests in milliseconds. Default
                        is 1000ms.
  -c COUNT, --count=COUNT
                        count of requests. if not specified -- there's no
                        limit.
```
