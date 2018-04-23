#!/usr/bin/env python3

# SPDX-License-Identifier: MIT

import base64
import getpass
import json
import os
import requests
import sys

token = ''


def get_token():
    try:
        config = json.load(open(os.path.expanduser("~/.docker/config.json")))
    except IOError as err:
        logging.error('Error accessing Docker auth file: {0}'.format(err))
        sys.exit(1)

    try:
        username, password = base64.b64decode(
            config['auths']['hub.docker.com']['auth']
            ).decode('utf-8').split(':')
    except KeyError:
        username = input('Enter Docker hub username: ')
        password = getpass.getpass('Enter Docker hub password: ')

    r = requests.post('https://hub.docker.com/v2/users/login/',
            data={'username': username, 'password': password})

    token = ""
    if r.status_code == 200:
        token = r.json()['token']
    else:
        print('Authorization failed', file=sys.stderr)
        sys.exit(2)

    return token


def del_tag(namespace, repo, tag):
    url = 'https://hub.docker.com/v2/repositories/%s/%s/tags/%s/' % \
        (namespace, repo, tag)

    r = requests.delete(url, headers={
        'Authorization': 'JWT %s' % token})

    if r.status_code == 204:
        print('{0}/{1}:{2} removed'.format(namespace, repo, tag))


def main(namespace, repo, tag=''):
    global token
    token = get_token()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(*sys.argv[1:])
