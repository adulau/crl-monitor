#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import pypssl
import json


def main():
    parser = argparse.ArgumentParser(description='Query a Passive SSL instance.')
    parser.add_argument("--url", default='https://www.circl.lu/', help='URL where the passive SSL is running (no path).')
    parser.add_argument("-v", "--version", type=int, default=2, help='URL where the passive SSL is running (no path).')
    parser.add_argument("-u", "--username", help='Username to login on the platform.')
    parser.add_argument("-p", "--password", help='Password to login on the platform.')
    parser.add_argument("-t", "--token", help='Token to login on the platform.')
    parser.add_argument("-i", "--ip", help='IP to query (can be a block, max /23).')
    parser.add_argument("-c", "--cert", help='SHA1 of the certificate to search.')
    parser.add_argument("-f", "--fetch", help='SHA1 of the certificate to fetch.')
    args = parser.parse_args()

    p = pypssl.PyPSSL(args.url, args.version, (args.username, args.password), args.token)

    if args.ip is not None:
        print(json.dumps(p.query(args.ip)))
    elif args.cert is not None:
        print(json.dumps(p.query_cert(args.cert)))
    elif args.fetch is not None:
        print(json.dumps(p.fetch_cert(args.fetch, make_datetime=False)))
    else:
        print('You didn\'t query anything...')


if __name__ == '__main__':
    main()
