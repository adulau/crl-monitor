#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import socket


class PyPSSL(object):

    def __init__(self, url='https://www.circl.lu/pssl/query', basic_auth=None,
                 auth_token=None):
        self.url = url

        self.session = requests.Session()
        if basic_auth is not None:
            # basic_auth has do be a tuple ('user_name', 'password')
            self.session.auth = basic_auth
        elif auth_token is not None:
            self.session.headers.update({'Authorization': auth_token})
        else:
            # No authentication defined.
            pass

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

    def query(self, q):
        check = self._check_IP(q)
        if check is not None:
            return check
        response = self.session.get('{}/{}' .format(self.url, q))
        try:
            return response.json()
        except:
            raise Exception('Unable to decode JSON object: ' + response.text)
        return {}
