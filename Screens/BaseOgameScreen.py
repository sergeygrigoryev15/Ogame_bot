from selenium.webdriver.common.by import By

from Core.BaseScreen import BaseScreen
from Elements.FleetAlertsTab import FleetAlertsTab
from Elements.NavigationMenu import NavigationMenu
from Elements.PlanetsList import PlanetsList
from Elements.ResourcesTab import ResourcesTab
from Elements.WebElement import WebElement

XPATH = '//*[@id="pageReloader"]'


class BaseOgameScreen(BaseScreen):
    def __init__(self, xpath=XPATH):
        BaseScreen.__init__(self, xpath)

        self.resources_tab = ResourcesTab()
        self.navigation_menu = NavigationMenu()
        self.planets_list = PlanetsList()
        self.fleetAlertsTab = FleetAlertsTab()

    @staticmethod
    def return_to_overview():
        WebElement('pageReloader', By.ID).click()

    @property
    def resources(self):
        return self.resources_tab.data

    @property
    def planets(self):
        return self.planets_list.data

    @property
    def active_planet(self):
        return self.planets_list.active_planet

    def select_planet(self, planet: str):
        self.planets_list.select_planet(planet)
