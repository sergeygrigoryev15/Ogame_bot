import time

from Core.BaseScreen import BaseScreen
from Elements.WebElement import WebElement


class HubScreen(BaseScreen):

    def __init__(self):
        BaseScreen.__init__(self, '//*[@id="hub"]')

        self.btn_continue = WebElement('//button[contains(@class, "button-default")]')

    def continue_game(self):
        self.btn_continue.click()
        window_after = self.driver.window_handles[-1]
        time.sleep(5)
        self.driver.close()
        self.driver.switch_to_window(window_after)
