## -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
import yaml
import lamvery

try:
    with open(lamvery.secret.file('config.yml')) as f:
        _oauth_conf = yaml.load(f)

except Exception as e:
    print(e)

CONSUMER_KEY = _oauth_conf['consumer_key']
CONSUMER_SECRET = _oauth_conf['consumer_secret']
ACCESS_TOKEN = _oauth_conf['access_token']
ACCESS_SECRET = _oauth_conf['access_secret']
UA = _oauth_conf['ua']

MSTDN_CONSUMER_KEY = lamvery.secret.file('consumer_key.txt')
MSTDN_ACCESS_KEY = lamvery.secret.file('access_key.txt')

DOMAIN = 'http://cookpad.com'
END_POINT = '/recipe/hot'
BUCKET = 'recipe.aoshiman.org'
MSTDN_BASE_URL = 'https://mstdn.jp'
