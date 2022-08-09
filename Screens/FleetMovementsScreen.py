import re

from Elements.WebElement import WebElement
from Screens.BaseOgameScreen import BaseOgameScreen


class FleetMovementInfo:
    def __init__(self, element):
        self.element = element
        self.additionalXpathPattern = "/*[contains(@class, '{}')]"
        self.base_id = self.element.get_attribute('id')

        self.mission_type = self.element.get_attribute('data-mission-type')

        self.is_return = self.element.get_attribute('data-return-flight') == '1'

        self.arrival_time = self.element.get_attribute('data-arrival-time')

        self.from_planet = self.element.find_element_by_xpath(
            '.'
            + self.additionalXpathPattern.format('originData')
            + self.additionalXpathPattern.format('originPlanet')
        ).get_text()

        self.from_coordinates = self.element.find_element_by_xpath(
            '.'
            + self.additionalXpathPattern.format('originData')
            + self.additionalXpathPattern.format('originCoords')
        ).get_text()

        self.to_planet = self.element.find_element_by_xpath(
            '.'
            + self.additionalXpathPattern.format('destinationData')
            + self.additionalXpathPattern.format('destinationPlanet')
        ).get_text()

        self.to_coordinates = self.element.find_element_by_xpath(
            '.'
            + self.additionalXpathPattern.format('destinationData')
            + self.additionalXpathPattern.format('destinationCoords')
        ).get_text()

        self.btn_reverse = WebElement(
            f'//*[@id="{self.base_id}"]'
            + self.additionalXpathPattern.format('reversal')
        )

    @property
    def id(self):
        regex = r'fleet(\d+)'
        match = re.match(regex, self.base_id)
        if match:
            return match.group(1)
        return self.base_id

    def reverse(self):
        self.btn_reverse.click()

    def __str__(self):
        return {
            'mission_type': self.mission_type,
            'is_return': self.is_return,
            'arrival_time': self.arrival_time,
            'from_planet': self.from_planet,
            'from_coordinates': self.from_coordinates,
            'to_planet': self.to_planet,
            'to_coordinates': self.to_coordinates,
        }


class FleetMovementsScreen(BaseOgameScreen):
    def __init__(self):
        BaseOgameScreen.__init__(self, '//*[@id="movement"]')

        self.btn_refresh = WebElement('//*[contains(@class, "icon_reload")]')

        self.fleet_details_elem = '//*[contains(@class, "fleetDetails")]'

    def refresh(self):
        self.btn_refresh.click()

    @property
    def event_log(self):
        return [
            FleetMovementInfo(el) for el in WebElement(self.fleet_details_elem).elements
        ]

    def get_log(self):
        return [el.__str__() for el in self.event_log]

    def return_fleet(self, **fleet_data):
        # TODO now supports only from_coordinates. Fix this.
        log = self.event_log
        for param in [
            'from_coordinates',
            # 'to_coordinates',
            # 'mission_type',
            # 'arrival_time',
        ]:
            if param in fleet_data.keys():
                value = fleet_data[param]
                return_fleet = WebElement('//*[contains(@class, "fleetDetails")][.//*[contains(.,"{}")]]'
                                          '//a[contains(@href, "component=movement&return=")]'.format(value))
                return_fleet.click()
                return
        else:
            self.notification_bot.message_me(f'Could not return fleet with data "{fleet_data}"\n'
                                             f'{[el.__str__() for el in log]}')
