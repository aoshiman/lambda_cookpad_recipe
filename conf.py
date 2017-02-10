# -*- coding: utf-8 -*-

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

class ParseConf(object):

    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configparser.RawConfigParser()
        self.config.read(self.config_file)


    def get_sections(self):
        sections = self.config.sections()
        return sections


    def get_items(self, account):
        items = self.config.items(account)
        return dict(items)


    def get_token(self, account, token):
        try:
            token = self.config.get(account, token)
        except:
            token = None
        return token
