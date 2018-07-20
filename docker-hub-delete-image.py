#!/usr/bin/env python3

# SPDX-License-Identifier: MIT

import http.client
import logging
import requests
import sys

from common import *

http.client.HTTPConnection.debuglevel = 0

# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True


def del_image(namespace, repo):
    url = 'https://hub.docker.com/v2/repositories/{0}/{1}/'.format(
            namespace, repo)

    logging.debug('Removing {0}/{1}'.format(namespace, repo))

    r = requests.delete(url, headers={
        'Authorization': 'JWT {0}'.format(token)})

    if r.status_code in fine_return_codes:
        print('{0}/{1} removed'.format(namespace, repo))


def main(namespace, repo, tag=''):
    global token
    token = get_token()

    images = get_images(namespace, repo)
    for image in images:
        if image['name'].startswith(repo):
            del_image(namespace, image['name'])

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(*sys.argv[1:])
