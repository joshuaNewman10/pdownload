from argparse import ArgumentParser
from functools import partial
from itertools import imap
from multiprocessing import Pool, cpu_count
import os
import socket
import string
import urllib2
import sys
from urlparse import urlparse

SUCCESS = 'SUCCESS'
FAILURE = 'FAILURE'
DUPLICATE = 'DUPLICATE'


def get_file_name(url):
    result = urlparse(url)
    return '_'.join(result.path.split('/'))


def download(url, timeout):
    fn = get_file_name(url)
    if os.path.exists(fn):
        return url, DUPLICATE, None

    try:
        response = urllib2.urlopen(url, timeout=timeout)
        with open(fn, 'wb') as im_file:
            im_file.write(response.read())
        return url, SUCCESS, None
    except Exception as e:
        if os.path.exists(fn):
            os.remove(fn)
        return url, FAILURE, e.message


def main():
    parser = ArgumentParser()
    parser.add_argument('--concurrency', '-c', type=int, default=cpu_count() - 1)
    parser.add_argument('--timeout', '-t', type=int, default=socket.getdefaulttimeout())
    parser.add_argument('--quiet', '-q', action='store_true')
    args = parser.parse_args()

    p = Pool(args.concurrency)
    func = partial(download, timeout=args.timeout)
    urls = imap(string.strip, sys.stdin)
    for url, status, e in p.imap_unordered(func, urls):
        if not args.quiet:
            print status + ':', url
            if e:
                print e


if __name__ == '__main__':
    main()