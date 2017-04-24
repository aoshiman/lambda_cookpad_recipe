# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from twython import Twython, TwythonError
from mastodon import Mastodon
import requests
from bs4 import BeautifulSoup
from boto3 import Session
from settings import config as cfg


def get_recipes():
    headers = {'User-Agent': cfg['UA']}
    response = requests.get(cfg['DOMAIN'] + cfg['END_POINT'], headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    recipes = []
    for tag in soup.find_all('a', {'class': 'recipe'}):
        recipes.append([tag.find('h2', {'class': 'recipe-title'}).text.rstrip('\n')\
                                                                    , tag['href']])
        recipes.reverse()
    return recipes


def get_recipe_list(bucket):
    s3 = Session().resource('s3')
    bucket = s3.Bucket(bucket)
    return [obj.key for obj in bucket.objects.all()]


def put_recipe(bucket, keyname):
    s3 = Session().resource('s3')
    bucket = s3.Bucket(bucket)
    obj = bucket.Object(keyname)
    body = keyname
    response = obj.put(
            Body=body.encode('utf-8'),
            ContentEncoding='utf-8',
            ContentType='text/plane'
            )


def tweet_recipe():
    """OAuth setting and Twit(if recipe is new)"""
    twitter = Twython(
                      cfg['CONSUMER_KEY'],
                      cfg['CONSUMER_SECRET'],
                      cfg['ACCESS_TOKEN'],
                      cfg['ACCESS_SECRET']
                      )

    mastodon = Mastodon(client_id=cfg['MSTDN_CONSUMER_KEY'],
                        access_token=cfg['MSTDN_ACCESS_KEY'],
                        api_base_url=cfg['MSTDN_BASE_URL']
                        )

    recipes = get_recipes()
    try:
        recipe_list = get_recipe_list(cfg['BUCKET'])
    except:
        pass

    for recipe in recipes:
        title, url, num = recipe[0], recipe[1], recipe[1].split('/')[2]
        if num not in recipe_list:
            post = u'{0} {1}'.format(title, cfg['DOMAIN'] + url)
            try:
                twitter.update_status(status=post)
                mastodon.status_post(post, visibility='private')
                print(post)
            except TwythonError as e:
                print(e)
            finally:
                put_recipe(cfg['BUCKET'], num)


def lambda_handler(event, context):
    tweet_recipe()


if __name__ == '__main__':
    tweet_recipe()
