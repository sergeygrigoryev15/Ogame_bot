import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Bot.SlackBot import bot
from Core.DbUtils import DbUtils

global web_driver
web_driver = None

global database
database = None


class BaseEntity(object):

    def __init__(self):
        self.URL = 'http://ogame.ru'
        self.slack_bot = bot
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")

    @property
    def driver(self):
        global web_driver
        if web_driver:
            return web_driver
        else:
            web_driver = webdriver.Chrome(os.path.abspath(__file__) + '/../../resources/chromedriver.exe',
                                          chrome_options=self.chrome_options)
        return web_driver

    @property
    def db(self):
        global database
        if not database:
            database = DbUtils()
        return database

    def init(self):
        self.driver.maximize_window()
        self.driver.get(self.URL)
