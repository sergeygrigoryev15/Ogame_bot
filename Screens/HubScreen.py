import time

from Core.BaseScreen import BaseScreen
from Elements.WebElement import WebElement

XPATH = '//*[@id="hub"]'


class HubScreen(BaseScreen):
    def __init__(self):
        BaseScreen.__init__(self, XPATH)

        self.btn_continue = WebElement('//button[contains(@class, "button-default")]')

    @staticmethod
    def is_open():
        return WebElement(XPATH).is_present()

    def continue_game(self):
        self.btn_continue.click()
        time.sleep(5)
        self.driver.close()
        self.driver.switch_to_window(self.driver.window_handles[-1])
