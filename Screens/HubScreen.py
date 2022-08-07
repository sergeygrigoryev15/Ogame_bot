import time
from typing import Optional

from selenium.webdriver.common.by import By

from Core.BaseScreen import BaseScreen
from Core.Env import environ
from Elements.WebElement import WebElement

XPATH = '//*[@id="hub"]'


class HubScreen(BaseScreen):
    def __init__(self):
        BaseScreen.__init__(self, XPATH)

        self.btn_continue = WebElement('//button[contains(@class, "button-default")]')
        self.btn_play = WebElement('//button[contains(@class, "button-primary")]')
        self.my_accounts = WebElement('myAccounts', By.ID)

        self.tmp_continue_in_universe = './/*[@role="rowgroup"]' \
                                        '[.//*[contains(@class, "server-name")]/*[contains(.,"{}")]]//button'

    @staticmethod
    def is_open():
        return WebElement(XPATH).is_present()

    def continue_game(self, universe: Optional[str] = environ('UNIVERSE', default=None)):
        time.sleep(3)
        if universe:
            self.btn_play.click()
            time.sleep(1)
            btn = self.my_accounts.find_element_by_xpath(self.tmp_continue_in_universe.format(universe))
            btn.click()
        else:
            self.btn_continue.click()
        time.sleep(3)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])