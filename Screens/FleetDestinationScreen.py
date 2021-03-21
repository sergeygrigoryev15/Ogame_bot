import time

from selenium.webdriver.common.by import By

from Elements.WebElement import WebElement
from Enums.ObjectTypes import ObjectTypes
from Screens.BaseOgameScreen import BaseOgameScreen


class FleetDestinationScreen(BaseOgameScreen):
    def __init__(self):
        BaseOgameScreen.__init__(self, '//*[@id="fleet2"]')

        self.speed_template = '//*[@id="speedPercentage"]//*[contains(@class, "step")]'
        self.planet_option = '//*[contains(@class, "dropdown")]/li[contains(.,"{}")]'

        self.btn_continue = WebElement('continueToFleet3', id_type=By.ID)
        self.btn_back = WebElement('backToFleet1', id_type=By.ID)

        self.txb_galaxy = WebElement('galaxy', id_type=By.ID)
        self.txb_system = WebElement('system', id_type=By.ID)
        self.txb_planet = WebElement('position', id_type=By.ID)

        self.select_planet = WebElement('//*[./*[@id="slbox"]]')

    def go_next(self):
        self.btn_continue.click()

    def select_speed(self, speed):
        WebElement(self.speed_template + f'[.="{speed}"]').click()

    @property
    def speed(self):
        return WebElement(
            self.speed_template + '[contains(@class, "selected")]'
        ).get_text()

    def select_destination(self, planet, object_type: ObjectTypes = ObjectTypes.PLANET):
        WebElement(f'{object_type.value}button', id_type=By.ID).click()
        if isinstance(planet, str):
            self.select_planet.click()
            time.sleep(2)
            WebElement(self.planet_option.format(planet)).click()
        elif isinstance(planet, list) or isinstance(planet, tuple):
            galaxy, system, planet = planet
            self.txb_galaxy.send_keys(galaxy)
            self.txb_system.send_keys(system)
            self.txb_planet.send_keys(planet)
