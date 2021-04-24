from Core.BaseTest import BaseTest
from Elements.NavigationMenu import MenuTabs
from Enums.Resources import Resources
from Screens.OverviewScreen import OverviewScreen


class Test(BaseTest):
    def run_test(self):
        overview_screen = OverviewScreen()
        resources_data = overview_screen.resources_tab.data
        parsed_data = [dict({'Type': name}, **value) for name, value in resources_data.items()]
        self.logger.make_table([row for row in parsed_data if row.get('Type') in
                                [Resources.METAL, Resources.CRYSTAL, Resources.DEUTERIUM]])
        overview_screen.navigation_menu.open_tab(MenuTabs.RESOURCES)
        self.logger.info(overview_screen.navigation_menu.active_tab)
        self.logger.info(overview_screen.planets_list.active_planet)
        self.logger.info(overview_screen.planets_list.data)


if __name__ == '__main__':
    test = Test()
    test()
