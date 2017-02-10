## -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from ast import literal_eval
import lamvery

UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E238 Safari/601.1"
DOMAIN = 'http://cookpad.com'
END_POINT = '/recipe/hot'
BUCKET = 'recipe.aoshiman.org'

try:
    _oauth_conf = literal_eval(lamvery.secret.get('secret'))
    CONSUMER_KEY = _oauth_conf['CONSUMER_KEY']
    CONSUMER_SECRET = _oauth_conf['CONSUMER_SECRET']
    ACCESS_TOKEN = _oauth_conf['ACCESS_TOKEN']
    ACCESS_SECRET = _oauth_conf['ACCESS_SECRET']

except Exception as e:
    print(e)
