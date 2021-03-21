from selenium.webdriver.common.by import By

from Core.BaseScreen import BaseScreen
from Core.Env import environ, env
from Elements.WebElement import WebElement


class LoginScreen(BaseScreen):

    def __init__(self):
        BaseScreen.__init__(self, '//*[@id="loginRegisterTabs"]')

        self.tab_login = WebElement('//*[@class="tabsList"]/*[1]')
        self.email = WebElement('email', By.NAME)
        self.password = WebElement('password', By.NAME)
        self.submit = WebElement('//button[@type="submit"]')

    def login(self, login=None, password=None):
        self.tab_login.click()
        self.email.send_keys(login if login else environ(env.str, 'EMAIL'))
        self.password.send_keys(password if password else environ(env.str, 'PASSWORD'))
        self.submit.click()
