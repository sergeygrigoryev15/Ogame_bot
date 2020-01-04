import os
from selenium.webdriver.common.by import By

from Core.BaseScreen import BaseScreen
from Elements.WebElement import WebElement


class LoginScreen(BaseScreen):

    def __init__(self):
        BaseScreen.__init__(self, '//*[@id="loginRegisterTabs"]')

        self.tab_login = WebElement('//*[@class="tabsList"]/*[1]')
        self.email = WebElement('email', By.NAME)
        self.password = WebElement('password', By.NAME)
        self.submit = WebElement('//button[@type="submit"]')

    def login(self, login=os.getenv('EMAIL'), password=os.getenv('PASSWORD')):
        self.tab_login.click()
        self.email.send_keys(login)
        self.password.send_keys(password)
        self.submit.click()
