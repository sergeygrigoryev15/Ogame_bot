from Core.BaseScreen import BaseScreen
from Elements.FleetAlertsTab import FleetAlertsTab
from Elements.NavigationMenu import NavigationMenu
from Elements.PlanetsList import PlanetsList
from Elements.ResourcesTab import ResourcesTab


class BaseOgameScreen(BaseScreen):
    def __init__(self, xpath):
        BaseScreen.__init__(self, xpath)

        self.resources_tab = ResourcesTab()
        self.navigation_menu = NavigationMenu()
        self.planets_list = PlanetsList()
        self.fleetAlertsTab = FleetAlertsTab()

    @property
    def resources(self):
        return self.resources_tab.data
