import base64
import getpass
import json
import logging
import os
import requests
import sys

token = ''

fine_return_codes = [requests.codes.ok, requests.codes.accepted,
                     requests.codes.no_content]


def get_images(namespace, repo):
    base = "https://hub.docker.com/v2/repositories"
    r = requests.get("{0}/{1}/?page_size=100".format(base, namespace))
    jsondata = r.json()
    data = jsondata['results']

    while jsondata['next']:
        logging.info('fetching another set...')
        jsondata = requests.get(jsondata['next']).json()
        data += jsondata['results']

    return data


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
