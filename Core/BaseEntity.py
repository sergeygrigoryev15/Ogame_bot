import re

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Bot.TelegramBot import TelegramBot
from Core.DbUtils import DbUtils
from Core.Env import environ, env
from Core.HttpUtils import HttpUtils
from Core.Logger import Logger

global web_driver
web_driver = None

global database
database = None

global httpClient
httpClient = None

chromedriver_autoinstaller.install()


class BaseEntity(object):
    def __init__(self):
        self.URL = 'http://ogame.ru'
        self.notification_bot = TelegramBot
        self.logger = Logger()
        self.chrome_options = Options()
        if environ('HEADLESS', env.bool, False):
            self.chrome_options.add_argument("--headless")

    @property
    def driver(self):
        global web_driver
        if web_driver:
            return web_driver
        else:
            web_driver = webdriver.Chrome(chrome_options=self.chrome_options)
        return web_driver

    @property
    def db(self):
        global database
        if not database:
            database = DbUtils()
        return database

    @property
    def http(self):
        global httpClient
        if not httpClient:
            url_reg = r'(http?s://.*com)/.*'
            match = re.match(url_reg, self.driver.current_url)
            assert match, f'Could not parse base url {self.driver.current_url}'
            httpClient = HttpUtils(match.group(1))
        return httpClient

    def init(self):
        self.driver.maximize_window()
        self.driver.get(self.URL)
