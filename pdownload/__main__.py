from argparse import ArgumentParser
from functools import partial
from itertools import imap
from multiprocessing import Pool, cpu_count
import os
import json
import socket
import string
import urllib2
import sys
from urlparse import urlparse

SUCCESS = 'SUCCESS'
FAILURE = 'FAILURE'
DUPLICATE = 'DUPLICATE'


def load_json_file(file_name):
    with open(file_name) as f:
        data = json.load(file_name)

    for datum in data:
        yield datum


def get_file_name(url):
    result = urlparse(url)
    return '_'.join(result.path.split('/'))


def download(url_data, timeout):
    url = url_data['url']
    id = url_data['id']
    if os.path.exists(url):
        return url, DUPLICATE, None

    try:
        response = urllib2.urlopen(url, timeout=timeout)
        with open(url, 'wb') as im_file:
            im_file.write(response.read())
            os.rename(url, id)
        return url, SUCCESS, None
    except Exception as e:
        if os.path.exists(url):
            os.remove(url)
        return url, FAILURE, e.message


def main():
    parser = ArgumentParser()
    parser.add_argument('file_name')
    parser.add_argument('--concurrency', '-c', type=int, default=cpu_count() - 1)
    parser.add_argument('--timeout', '-t', type=int, default=socket.getdefaulttimeout())
    parser.add_argument('--quiet', '-q', action='store_true')
    args = parser.parse_args()

    p = Pool(args.concurrency)
    func = partial(download, timeout=args.timeout)
    urls = load_json_file(args.file_name)
    for url, status, e in p.imap_unordered(func, urls):
        if not args.quiet:
            print status + ':', url
            if e:
                print e


if __name__ == '__main__':
    main()