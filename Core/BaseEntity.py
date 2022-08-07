import re
import time

from selenium.webdriver.android.webdriver import WebDriver
from tqdm import trange

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Bot.TelegramBot import TelegramBot
from Core.DbUtils import DbUtils
from Core.Env import environ, env
from Core.HttpUtils import HttpUtils
from Core.Logger import Logger

# TODO get rid of global variables
global web_driver
web_driver = None

global database
database = None

global http_client
http_client = None

chromedriver_autoinstaller.install()


class BaseEntity:
    notification_bot = TelegramBot()
    url = 'http://ogame.ru'
    logger = Logger()

    def __init__(self):
        self.chrome_options = Options()
        if environ('HEADLESS', env.bool, False):
            self.chrome_options.add_argument("--headless")

    @property
    def driver(self) -> WebDriver:
        global web_driver
        if web_driver:
            return web_driver
        else:
            web_driver = webdriver.Chrome(chrome_options=self.chrome_options)
        return web_driver

    @property
    def db(self) -> DbUtils:
        global database
        if not database:
            database = DbUtils()
        return database

    @property
    def http(self) -> HttpUtils:
        global http_client
        if not http_client:
            url_reg = r'(http?s://.*com)/.*'
            match = re.match(url_reg, self.driver.current_url)
            assert match, f'Could not parse base url {self.driver.current_url}'
            http_client = HttpUtils(match.group(1))
        return http_client

    def sleep(self, timeout: int) -> None:
        self.logger.debug(f'sleep {timeout} seconds')
        for _ in trange(timeout):
            time.sleep(1)

    def init(self) -> None:
        self.driver.maximize_window()
        self.driver.get(self.url)
