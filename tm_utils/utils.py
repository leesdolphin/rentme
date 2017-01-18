

import asyncio
from collections import OrderedDict
import http.cookies
import itertools
import json
import sys

from multidict import CIMultiDict
import aiohttp


class NullCookieJar(aiohttp.cookiejar.CookieJar):

    def update_cookies(self, *a, **k):
        return

    def __iter__(self):
        return iter([])

    def __len__(self):
        return 0


def parse_headers_from_stdin():
    headers = CIMultiDict()
    host = None
    path = None
    blank_count = 0
    for line in sys.stdin:
        line = line.strip()
        if not line:
            blank_count += 1
            if blank_count >= 2:
                break
        if line.startswith('GET'):
            _, _, path = line.partition('GET ')
        else:
            name, _, value = line.partition(': ')
            if name == 'Host':
                host = value
            else:
                headers[name] = value
    if host is None or path is None:
        raise ValueError('Invalid input. could not find host or path.')
    return 'http://{}{}'.format(host, path), headers


def parse_cookies(header):
    if not isinstance(header, str):
        return []
    return header.split('; ')
