#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import socket
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin
import dateutil.parser


class PyPSSL(object):

    def __init__(self, base_url='https://www.circl.lu/', api_version=2, basic_auth=None, auth_token=None):
        self.base_url = base_url
        self.api_version = api_version

        self.session = requests.Session()
        if basic_auth is not None:
            # basic_auth has do be a tuple ('user_name', 'password')
            self.session.auth = basic_auth
        elif auth_token is not None:
            self.session.headers.update({'Authorization': auth_token})
        else:
            # No authentication defined.
            pass

    def _query(self, url, timeout=None):
        response = self.session.get(url, timeout=timeout)
        try:
            return response.json()
        except:
            raise Exception('Unable to decode JSON object: ' + response.text)

    def _check_IP(self, ip):
        if ':' in ip:
            return {'error': 'IPv6 is not (yet) supported'}
        splitted = ip.split('/')
        try:
            if len(splitted) == 2:
                ip, block = splitted
                if int(block) < 23:
                    return {'error': 'Maximum CIDR block size reached >/23'}
            socket.inet_aton(ip)
        except:
            return {'error': 'Incorrect format'}
        return None

    def query(self, q, timeout=None):
        check = self._check_IP(q)
        if check is not None:
            return check
        if self.api_version == 1:
            path = 'pssl/query/{}'.format(q)
        else:
            path = 'v2pssl/query/{}'.format(q)
        return self._query(urljoin(self.base_url, path), timeout=timeout)

    def query_cert(self, q, timeout=None):
        if self.api_version != 2:
            return {'error': 'Only available in API v2'}
        path = 'v2pssl/cquery/{}'.format(q)
        return self._query(urljoin(self.base_url, path), timeout=timeout)

    def fetch_cert(self, q, make_datetime=True, timeout=None):
        if self.api_version != 2:
            return {'error': 'Only available in API v2'}
        path = 'v2pssl/cfetch/{}'.format(q)
        response = self._query(urljoin(self.base_url, path), timeout=timeout)
        if response.get('error') or not make_datetime:
            return response
        # create python datetime, doesn't return a json object
        response['info']['not_before'] = dateutil.parser.parse(response['info']['not_before'])
        response['info']['not_after'] = dateutil.parser.parse(response['info']['not_after'])
        return response
