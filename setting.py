## -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
import yaml
import lamvery

UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E238 Safari/601.1"
DOMAIN = 'http://cookpad.com'
END_POINT = '/recipe/hot'
BUCKET = 'recipe.aoshiman.org'

try:
    with open(lamvery.secret.file('config.yml')) as f:
        _oauth_conf = yaml.load(f)

except Exception as e:
    print(e)

CONSUMER_KEY = _oauth_conf['consumer_key']
CONSUMER_SECRET = _oauth_conf['consumer_secret']
ACCESS_TOKEN = _oauth_conf['access_token']
ACCESS_SECRET = _oauth_conf['access_secret']
