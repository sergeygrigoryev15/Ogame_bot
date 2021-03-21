import time
from datetime import datetime

from selenium.webdriver.common.by import By

from Elements.WebElement import WebElement
from Enums.FleetMissionTypes import FleetMissionTypes

DATE_FORMAT = '%d.%m %H:%M:%S'


class BattleEvent(object):
    def __init__(self, element):
        self.element = element
        self.additionalXpathPattern = "./*[contains(@class, '{}')]"

        self.mission_type = self.element.get_attribute('data-mission-type')

        self.is_return = self.element.get_attribute('data-return-flight') == 'true'

        self.is_friendly = 'friendly' in self.element.find_element_by_xpath(
            self.additionalXpathPattern.format('countDown') + '/*[contains(@id, "counter-eventlist")]')\
            .get_attribute('class')

        self.arrival_time = datetime.fromtimestamp(int(self.element.get_attribute('data-arrival-time')))

        self.remaining_time = self.arrival_time - datetime.now()

        self.from_planet = self.element.find_element_by_xpath(
            self.additionalXpathPattern.format('originFleet')).get_text()

        self.from_coordinates = self.element.find_element_by_xpath(
            self.additionalXpathPattern.format('coordsOrigin')).get_text()

        self.to_planet = self.element.find_element_by_xpath(
            self.additionalXpathPattern.format('destFleet')).get_text()

        self.to_coordinates = self.element.find_element_by_xpath(
            self.additionalXpathPattern.format('destCoords')).get_text()

        self.fleet_size = self.element.find_element_by_xpath(
            self.additionalXpathPattern.format('detailsFleet')).get_int()

    def __str__(self):
        return {
            'mission_type': FleetMissionTypes(self.mission_type),
            'is_return': self.is_return,
            'arrival_time': self.arrival_time.strftime(DATE_FORMAT),
            'from_planet': self.from_planet,
            'from_coordinates': self.from_coordinates,
            'to_planet': self.to_planet,
            'to_coordinates': self.to_coordinates,
            'fleet_size': self.fleet_size,
            'is_friendly': self.is_friendly,
            'remaining_time': str(self.remaining_time)
        }


class FleetAlertsTab(WebElement):

    def __init__(self):
        self.xpath = '//div[@id="message-wrapper"]'
        WebElement.__init__(self, self.xpath)

        self.empty_fleet_list = WebElement('eventboxBlank', id_type=By.ID)
        self.messages = self.xpath + '//*[contains(@class, "msg_count")]'

    @property
    def is_alert(self):
        return WebElement('//*[@id="attack_alert"]').is_present()

    def open_messages_list(self):
        WebElement(self.messages).click()

    @property
    def messages_count(self):
        return int(WebElement(self.messages).element.get_attribute('data-new-messages'))

    @property
    def expanded(self):
        return WebElement('eventboxContent', By.ID).is_present()

    def __expand(self):
        if not self.expanded:
            for _ in range(5):
                WebElement(self.xpath).click()
                time.sleep(2)
                if self.expanded:
                    break

    def __collapse(self):
        if self.expanded:
            for _ in range(5):
                WebElement(self.xpath).click()
                time.sleep(2)
                if not self.expanded:
                    break

    @property
    def event_log(self):
        return [BattleEvent(el) for el in WebElement("//*[contains(@id, 'eventContent')]//tr").elements]

    def get_log(self):
        if self.empty_fleet_list.is_present():
            return []
        self.__expand()
        log = self.event_log
        self.__collapse()
        return log
