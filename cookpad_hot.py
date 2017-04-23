# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from twython import Twython, TwythonError
from mastodon import Mastodon
import requests
from bs4 import BeautifulSoup
from boto3 import Session
#  from setting import config as cfg
from setting import UA, DOMAIN, END_POINT, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET, MSTDN_CONSUMER_KEY, MSTDN_ACCESS_KEY, MSTDN_BASE_URL, BUCKET


def get_recipes():
    headers = {'User-Agent': UA}
    response = requests.get(DOMAIN + END_POINT, headers=headers)
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
                      CONSUMER_KEY,
                      CONSUMER_SECRET,
                      ACCESS_TOKEN,
                      ACCESS_SECRET
                      )

    mastodon = Mastodon(client_id=MSTDN_CONSUMER_KEY,
                        access_token=MSTDN_ACCESS_KEY,
                        api_base_url=MSTDN_BASE_URL
                        )

    recipes = get_recipes()
    try:
        recipe_list = get_recipe_list(BUCKET)
    except:
        pass

    for recipe in recipes:
        title, url, num = recipe[0], recipe[1], recipe[1].split('/')[2]
        if num not in recipe_list:
            post = u'{0} {1}'.format(title, DOMAIN + url)
            try:
                twitter.update_status(status=post)
                mastodon.status_post(post, visibility='private')
                print(post)
            except TwythonError as e:
                print(e)
            finally:
                put_recipe(BUCKET, num)


def lambda_handler(event, context):
    tweet_recipe()


if __name__ == '__main__':
    tweet_recipe()
