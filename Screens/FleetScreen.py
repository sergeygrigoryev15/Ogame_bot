from selenium.webdriver.common.by import By

from Elements.WebElement import WebElement
from Screens.BaseOgameScreen import BaseOgameScreen


class FleetScreen(BaseOgameScreen):
    def __init__(self):
        BaseOgameScreen.__init__(self, '//*[@id="fleet1"]')

        self.btn_select_all = WebElement('sendall', id_type=By.ID)
        self.btn_select_none = WebElement('resetall', id_type=By.ID)
        self.btn_continue = WebElement('continueToFleet2', id_type=By.ID)

        self.lbl_warning_no_fleet = WebElement('warning', By.ID)

    @property
    def has_fleet(self):
        return not self.lbl_warning_no_fleet.is_present()

    def select_all(self):
        self.btn_select_all.click()

    def go_next(self):
        self.btn_continue.click()
