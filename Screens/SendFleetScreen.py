import time
import re
from datetime import datetime
from typing import Union

from selenium.webdriver.common.by import By

from Elements.WebElement import WebElement
from Enums.FleetMissionTypes import FleetMissionTypes
from Enums.ObjectTypes import ObjectTypes
from Screens.BaseOgameScreen import BaseOgameScreen


PLANET_REGEX = r'\[?(\d{1}):(\d{1,3}):(\d{1,2})\]?'


class SendFleetScreen(BaseOgameScreen):
    def __init__(self):
        BaseOgameScreen.__init__(self, '//*[@id="fleet2"]')

        self.speed_template = '//*[@id="speedPercentage"]//*[contains(@class, "step")]'
        self.planet_option = '//*[contains(@class, "dropdown")]/li[contains(.,"{}")]'

        self.mission_type_template = '//*[@id="missions"]//*[@data-mission={}]'
        self.selected_mission_type = (
            '//*[@id="missions"]//a[contains(@class, "selected")]'
        )

        self.btn_back = WebElement('backToFleet1', id_type=By.ID)

        self.txb_galaxy = WebElement('galaxy', id_type=By.ID)
        self.txb_system = WebElement('system', id_type=By.ID)
        self.txb_planet = WebElement('position', id_type=By.ID)

        self.select_planet = WebElement('slbox', By.ID)

        self.btn_all_resources = WebElement('allresources', id_type=By.ID)

        self.btn_send_fleet = WebElement('sendFleet', id_type=By.ID)

    def select_speed(self, speed):
        WebElement(self.speed_template + f'[.="{speed}"]').click()

    @property
    def speed(self):
        return WebElement(
            self.speed_template + '[contains(@class, "selected")]'
        ).get_text()

    def select_destination(self, planet: Union[str, list, tuple], object_type: ObjectTypes = ObjectTypes.PLANET):
        WebElement(f'{object_type.value}button', id_type=By.ID).click()
        if isinstance(planet, str):
            match = re.match(PLANET_REGEX, planet)
            galaxy, system, planet = match.groups()
        else:
            galaxy, system, planet = planet
        time.sleep(2)
        self.txb_galaxy.send_keys(str(galaxy))
        self.txb_system.send_keys(str(system))
        self.txb_planet.send_keys(str(planet))

    def select_mission_type(self, mission_type: FleetMissionTypes = FleetMissionTypes.TRANSPORT):
        WebElement(self.mission_type_template.format(mission_type.value)).click()

    @property
    def selected_mission(self):
        return WebElement(self.selected_mission_type).get_attribute('data-mission')

    def put_all_resources(self):
        self.btn_all_resources.click()

    def send_fleet(self) -> datetime:
        self.btn_send_fleet.click()
        return datetime.now()
