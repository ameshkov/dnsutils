#!/usr/bin/python3

# A simple script that creates some constant load on a DNS server.

import requests
import zipfile
import tempfile
import os
import time
import dns.resolver
import sys
from optparse import OptionParser

# TOP_1M_URL = "http://s3.amazonaws.com/alexa-static/top-1m.csv.zip"
TOP_1M_URL = "http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip"
FILE_NAME = "top-1m.csv"


def get_top1m_domains():
    """Downloads the TOP1M domains and returns an array with them
    """

    print("Downloading {0}".format(TOP_1M_URL))
    r = requests.get(TOP_1M_URL)

    # Retrieve HTTP meta-data
    print("Response status={0} content-type={1}".format(r.status_code,
                                                        r.headers['content-type']))

    # Prepare the ZIP file
    with tempfile.TemporaryFile() as tmp_zip:
        tmp_zip.write(r.content)
        archive = zipfile.ZipFile(tmp_zip)

        # Extract it to a temp directory
        with tempfile.TemporaryDirectory() as tmp_dir:
            archive.extractall(tmp_dir)

            # Read the CSV file
            with open(os.path.join(tmp_dir, FILE_NAME), 'r') as tmp_csv:
                lines = tmp_csv.readlines()
                i = 0
                while i < len(lines):
                    parts = lines[i].split(",")
                    if (len(parts) == 2):
                        lines[i] = parts[1].strip()
                    i += 1
                return lines


def dns_loop(server, interval, count):
    """Makes DNS requests for the TOP 1M domains
    server - dns server to make the requests to
    interval - interval in milliseconds between requests
    count - max number of requests
    """

    print("Server is {0}".format(server))
    print("Interval is {0}ms".format(interval))
    if count == 0:
        print("Count is unlimited")
    else:
        print("Count is {0}".format(count))

    # create a resolver
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [server]

    # top 1M domains
    domains = get_top1m_domains()

    i = 0
    while i < 0 or count == 0:
        # get a domain
        domain = domains[i % len(domains)]

        try:
            resolver.query(domain)
        except:
            print("-", end='')
            sys.stdout.flush()
            # print("\nAn exception occurred while querying {0}".format(domain))

        # Print and sleep
        end = ''
        if i % 100 == 0:
            end = '\n'
        print(".", end=end)
        sys.stdout.flush()
        i += 1
        time.sleep(float(interval) / 1000)


def main():
    parser = OptionParser()
    parser.add_option("-s", "--server", dest="server", default="8.8.8.8",
                      help="DNS server address.")
    parser.add_option("-i", "--interval", dest="interval", type="int", default=1000,
                      help="interval between DNS requests in milliseconds. Default is 1000ms.")
    parser.add_option("-c", "--count", dest="count", type="int", default=0,
                      help="count of requests. if not specified -- there's no limit.")

    # pylint: disable=unused-variable
    (options, args) = parser.parse_args()

    dns_loop(options.server, options.interval, options.count)


# ENTRY POINT
main()
