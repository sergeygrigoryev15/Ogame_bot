from selenium.webdriver.common.by import By

from Elements.WebElement import WebElement
from Enums.FleetMissionTypes import FleetMissionTypes
from Screens.BaseOgameScreen import BaseOgameScreen


class FleetMissionScreen(BaseOgameScreen):

    def __init__(self):
        BaseOgameScreen.__init__(self, '//*[@id="fleet3"]')

        self.mission_type_template = '//*[@id="missions"]//*[@data-mission={}]'
        self.selected_mission_type = '//*[@id="missions"]//a[contains(@class, "selected")]'

        self.btn_all_resources = WebElement('allresources', id_type=By.ID)
        self.btn_send_fleet = WebElement('sendFleet', id_type=By.ID)

    def select_mission_type(self, mission_type=FleetMissionTypes.TRANSPORT):
        WebElement(self.mission_type_template.format(mission_type.value)).click()

    @property
    def selected_mission(self):
        return WebElement(self.selected_mission_type).get_attribute('data-mission')

    def put_all_resources(self):
        self.btn_all_resources.click()

    def send_fleet(self):
        self.btn_send_fleet.click()
